from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask,session,send_from_directory
from flask_mail import Mail,Message
from website.controller.securityController import *
import website.model.user_db as db
from .passwordController import PasswordController
from random import *
import random
import string
import secrets
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta, timezone
import MySQLdb
import requests
import json
import os

user = Blueprint('userController', __name__,template_folder='views')
app = Flask(__name__,static_url_path='/static')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_NAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'default_sender_email'
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['DEBUG'] = True

mail = Mail(app)

###### user sign up #####
def sign_up():
    try:
        if request.method == "POST":
            email = validate_email(request.form['email'])
            username = validate_allow_symbols(request.form['username'], "-_")
            dob = validate_date(request.form['dob'])
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            p = PasswordController()
            captcha_response = request.form['g-recaptcha-response']
            
            if not is_human(captcha_response):
                flash("Unknown error occured.", category="error")
                return redirect(url_for("userrouting.sign_up"))
                
            #Validation done in check_password()
            passwd_errors = p.check_password(password, confirmPassword)
            if passwd_errors:
                flash(str(passwd_errors), category="error")
            #Check unique email and username
            username_error = db.login_db(username)
            email_error = db.email_db(email)
            if username_error or email_error:
                flash("Username or E-mail already in use", category="error")
            #Check age is between 18 to 100
            dob = datetime.strptime(dob, "%Y-%m-%d")
            calculate_age = (datetime.now() - dob)// timedelta(days=365.2425)
            if int(calculate_age) < 18 or int(calculate_age) > 105:
                flash("Age should be between 18 to 105", category="error")
                return redirect(url_for("userrouting.sign_up"))
            if (not passwd_errors) and (not username_error) and (not email_error):
                password = p.hash_password(password)
                verification_token = get_random_string()
                signUpInsertdb = db.sign_up_db(email,username,password,dob,verification_token)
                #sending of email after no errors are found on the signup page parameters
                confirm_url = url_for('userrouting.confirmation', token=verification_token, _external=True, _scheme='https')
                template = render_template("user/confirmation.html", confirm_url=confirm_url)
                subject = "Please Confirm your email"
                msg = Message(subject,sender=os.environ.get('MAIL_NAME'), html=template, recipients=[email])
                mail.send(msg)
                flash('A confirmation email has been sent, please check your email', 'success')
                app.logger.info('%s successfully signed up, unverified', username)
		#setting parameters of the user after account creation, bring them over to the unverified account page
                session['loggedIn'] = True
                session['username'] = username
                session['verified'] = "0"
                return redirect(url_for('userrouting.unconfirmed'))
            else:
                flash("Something went wrong", category="error")
            return redirect(url_for("userrouting.sign_up"))
        return render_template("user/sign_up.html")
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return render_template("user/sign_up.html")      
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return render_template("user/sign_up.html")

###### capcha ######

def is_human(captcha_response):
    secret = os.environ.get('CAPTCHA_KEY')
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']

###### generate url link for otp/signup ######

def get_random_string():
    result_str = secrets.token_urlsafe(16)
    return result_str

###### handling unverified users after signup ######

def unconfirmed():
    if str(session.get('verified')) == "1":
        flash('Account already verified','success')
        return redirect(url_for('userrouting.home'))
    if session.get('verified') is None:
        flash('Please login again', 'error')
        session.pop('loggedIn', None)
        session.pop('username', None)
        return redirect(url_for('userrouting.login'))
    flash('Please verify your account', 'error')
    return render_template('user/unconfirmed.html')

###### confirmation of account ######

def confirmation(token):
    try:
        #handling of different scenarios, reroute to home page if they are verified
        if str(session['verified']) == "1":
            flash('Account already verified','success')
            return redirect(url_for('userrouting.home'))
        #error handling if verified is not set properly, reroute back to login and clear session
        if str(session['verified']) is None:
            flash('Please login again', 'error')
            session.pop('loggedIn', None)
            session.pop('username', None)
            return redirect(url_for('userrouting.login'))
        username = session['username']
        retrieved_info = db.login_db(username)
        verification_token = retrieved_info[6]
        verification_timestamp = retrieved_info[8]
        #calculating the time of OTP creation, OTP set to expire over 30 minutes
        current_date = datetime.now()
        time_difference = (current_date - verification_timestamp)
        total_seconds = time_difference.total_seconds()
        minutes = total_seconds/60
        #handling of expired verfication link
        if int(minutes) > 30:
            flash("Confirmation link timed out, please request another verification link", 'error')
            return redirect(url_for('userrouting.unconfirmed'))
        if str(verification_token) != str(token):
            flash("Invalid confirmation link", 'error')
            return redirect(url_for('userrouting.unconfirmed'))
        else:
            #successfully verfied link, changing parameters in db via a function
            flash("Successfully verified email", 'success')
            app.logger.info('%s successfully signed up, verified', username)
            reply = db.verification(username)
            db.clear_verification(username)
            session.clear()
            flash("Please log in again", 'success')
            return redirect(url_for('userrouting.login'))
        return render_template("user/confirmation.html")
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return redirect(url_for('userrouting.unconfirmed'))   
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return redirect(url_for('userrouting.unconfirmed'))

###### resending confirmation email ######
def resend_confirmation():
    try:
        if str(session['verified']) == "1":
            flash('Account already verified','success')
            return redirect(url_for('userrouting.home'))
        if str(session['verified']) is None:
            flash('Please login again', 'error')
            session.pop('loggedIn', None)
            session.pop('username', None)
            return redirect(url_for('userrouting.login'))
        #regenerating of a new url for verification 
        verification_token= get_random_string()
        username = session['username']
        db.verification_update(username,verification_token)
        retrieved_info = db.login_db(username)
        email = retrieved_info[1]
        confirm_url = url_for('userrouting.confirmation', token=verification_token, _external=True, _scheme='https')
        template = render_template("user/confirmation.html", confirm_url=confirm_url)
        subject = "Please Confirm your email"
        msg = Message(subject,sender=os.environ.get('MAIL_NAME'), html=template, recipients=[email])
        mail.send(msg)
        flash('Verification link has been resent to your email','success')
        return redirect(url_for('userrouting.unconfirmed'))
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return redirect(url_for('userrouting.unconfirmed'))
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return redirect(url_for('userrouting.unconfirmed'))

###### user login #####
@loginpage_handler
def login():
    try:
        otpValue = randint(000000,999999)
        if request.method == "POST":
            username = validate_text(request.form['username'])
            p = PasswordController()
            password = validate_allow_symbols(request.form['password'], p.get_allowed_chars())
            if username and password:
                retrieved_info = db.login_db(username)
                if retrieved_info is None:
                    flash("Incorrect credentials", 'error')
                    return redirect(url_for('userrouting.login'))
                if p.verify_hash(password, retrieved_info[3]):
                    session['loggedIn'] = True
                    session['username'] = retrieved_info[2]
                    session['userid'] = retrieved_info[0]
                    session['email'] = retrieved_info[1]                    
                    session['OTP_timestamp'] = datetime.now(timezone.utc)
                    session['verified'] = retrieved_info[7]
                    session['otp_lock'] = retrieved_info[10]
                    session['lockedout_counter'] = retrieved_info[11]
                    session['locked_out'] = 0

                    #not allowing user to log in after 5 failed attempts
                    if session.get('lockedout_counter') >= 5:
                        session.clear()
                        flash("Your account has been locked out, please contact the administrator.", 'error')
                        return redirect(url_for('userrouting.login'))
                    #not allowing user to log in with a locked out account
                    if session.get('otp_lock') == 1:                        
                        session.clear()
                        flash('Your account has been locked out, please contact the administrator.', category="error")
                        return redirect(url_for('userrouting.login'))
                    if str(session['verified']) != str("1"):
                        return redirect(url_for('userrouting.unconfirmed'))
                    #sending of email for OTP
                    email=str(session['email'])
                    msg = Message("OTP Verification",sender=os.environ.get('MAIL_NAME'),recipients=[email])
                    msg.body = "Your OTP is: "+str(otpValue)
                    mail.send(msg)
                    session['locked'] = "1"
                    #storing of OTP in DB for verification
                    db.store_otp(session.get('username'), otpValue)
                    db.reset_account_lock(session.get('username'))

                    app.logger.info('%s successfully logged in', username)
                    return redirect(url_for('userrouting.verify'))
                else:
                    session['username'] = retrieved_info[2]
                    session['lockedout_counter'] = retrieved_info[11]        
                    if session.get('lockedout_counter') >= 5:
                        session.clear()
                        flash("Your account has been locked out, please contact the administrator.", 'error')
                        app.logger.warning('%s has locked out', username)
                        return redirect(url_for('userrouting.login'))
                    else:
                        db.update_account_lock(session.get('username'))
                        flash("Incorrect username or password", 'error')
                        return redirect(url_for('userrouting.login'))
                    return redirect(url_for('userrouting.login'))
                                    
            session['loggedIn'] = False
            flash("Incorrect username or password", category="error")
            return redirect(url_for('userrouting.login'))
        return render_template("user/login.html")
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return render_template("user/login.html")     
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return render_template("user/login.html")

######  user OTP verify ######
@verify_handler
def verify():
    #If user has logged in and OTP verified, redirect them to homepage
    if int(session.get('locked')) == 0:
        return redirect(url_for('userrouting.home'))
    
    if 'loggedIn' in session and request.method == 'POST':
        otp = request.form['otp']
        current_date = datetime.now(timezone.utc)
        generated_date = session['OTP_timestamp']
        #comparing current time to the time stored in db, if it is not within 30 minutes, OTP is invalid
        time_difference = (current_date - generated_date)
        total_seconds = time_difference.total_seconds()
        minutes = total_seconds/60
        get_otp = db.login_db(session.get('username'))
        retrieved_otp = get_otp[9]       
        if int(minutes) > 30:
            flash('Please relogin and generate a new OTP', 'warning')
            session.clear()
            return redirect(url_for('userrouting.login'))
        if str(otp) == str(retrieved_otp):
            session['locked'] = "0"
            return redirect(url_for('userrouting.home'))
        else:
            #Adding 1 to locked out if OTP is wrong
            session['locked_out'] += 1
            message = "Invalid OTP, please try again. " + str(3 - int(session.get('locked_out'))) + " tries left"
            flash(message, 'error')
            if session.get('locked_out') >= 3:
                try:
                    db.enable_otp_lock(session.get('username'))
                    app.logger.warning("%s has been locked out.", session['username'])
                    session.clear()                    
                    flash("Your account has been locked out, please contact the administrator.", 'error')
                    return redirect(url_for('userrouting.login'))
                except MySQLdb.Error as ex: 
                    app.logger.error(ex)
                    app.logger.info('%s successfully logged out', session['username'])
                    session.clear()
                    flash("Database error occured, please log in again.", category="error") 
                    return redirect(url_for('userrouting.login'))
                except Exception as ex:
                    app.logger.error(ex)
                    app.logger.info('%s successfully logged out', session['username'])
                    session.clear()
                    flash("Unknown exception occured, please log in again", category="error")
                    return redirect(url_for('userrouting.login'))                        
        return redirect(url_for('userrouting.verify'))
    return render_template("user/verify.html")
    
######  user profile  #####
@loginauth_required
def profile():
    try:
        ##user profile db here
        userProfile_db = db.profile_db()
        return render_template("user/profile.html",account=userProfile_db)
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))

###### updating of profile #####
@loginauth_required
def update():
    try:
        if request.method == 'POST':
            bios = validate_text(request.form['bios'])
            if not bios:
                flash("Only the following characters are allowed: .,?!", category="error")
                return redirect(url_for('userrouting.profile'))
            ##user update db here
            db.update_db(bios)
            ##user retrieve profile db here
            retrieve_userProfile_db = db.profile_db()
            return render_template("user/profile.html",account=retrieve_userProfile_db)
        return redirect(url_for('userrouting.profile'))
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))    

###### reset or forget password #####

def forgetPassword():
    try:
        if request.method == "POST":
            email = request.form['email']
            retrieved_info = db.email_db(email)
            if retrieved_info is None:
                flash('An account recovery email has been sent to the email that was entered','success')
                return redirect(url_for('userrouting.login'))
            username = retrieved_info[2]
            verification_token= get_random_string()
            db.verification_update(username,verification_token)
            msg = Message("Forget Password",sender=os.environ.get('MAIL_NAME'),recipients=[email])
            msg.body = "Hey, sending you the reset password email link https://meok.sitict.net/newPassword/"+verification_token
            mail.send(msg)
            flash("An account recovery email has been sent to the email that was entered", "success")
            app.logger.info('%s sent an account recovery email', username)
            return redirect(url_for('userrouting.login'))
        return render_template("user/forgetPassword.html")
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return render_template("user/forgetPassword.html")      
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return render_template("user/forgetPassword.html")    

###### creation of new password #####
def newPassword(token):
    try:
        received_info = db.get_user_verification_db(token)
        # Check that token exists in DB, account is verified and that the token given matches the one in the DB
        if received_info is None or received_info[7] != 1 or token!=received_info[6]:
            flash("Invalid link", category="error")
            return redirect(url_for('userrouting.login'))
        username = received_info[2]
        verification_token = received_info[6]
        verification_timestamp = received_info[8]
        current_date = datetime.now()
        time_difference = (current_date - verification_timestamp)
        total_seconds = time_difference.total_seconds()
        minutes = total_seconds/60
        
        if int(minutes) > 30:
            flash("Confirmation link timed out, please request another verification link", 'error')
            return redirect(url_for('userrouting.login'))
        if str(verification_token) != str(token):
            flash("Invalid confirmation link", 'error')
            return redirect(url_for('userrouting.login'))
        if request.method == "POST":
            received_info_2 = db.get_user_verification_db(token)
            if received_info_2 is not None and received_info_2[7]==1 and token==received_info_2[6]:
                p = PasswordController()
                newpassword = request.form['password']
                confirmpassword = request.form['confirmPassword']
                email = received_info_2[1]
                username = received_info_2[2]
                newpass_errors = p.check_password(newpassword, confirmpassword)
                if not newpass_errors:
                    newpassword = p.hash_password(newpassword)
                    user_newPassword_db = db.newPassword_db(newpassword, email)
                    db.clear_verification(username)
                else:
                    flash(str(newpass_errors), category="error")
                    return render_template("user/newPassword.html")
            return redirect(url_for('userrouting.login'))
        return render_template("user/newPassword.html")
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return redirect(url_for('userrouting.login'))     
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return redirect(url_for('userrouting.login'))  

###### changing of password #####
@loginauth_required
def changePassword():
    try:
        if request.method == 'POST':
            newpassword = request.form['new_password']
            confirmpassword = request.form['confirm_new_password']
            p = PasswordController()
            currentpassword = validate_allow_symbols(request.form['current_password'], p.get_allowed_chars())
            retrieved_info = db.login_db(session["username"])
            current_password_check = p.verify_hash(str(currentpassword), retrieved_info[3])
            # Validation is done in check_password()
            changepass_errors = p.check_password(newpassword, confirmpassword)
            if not current_password_check:
                flash("Current password is wrong", category="error")
                app.logger.error('%s did not successfully change password (Current password is wrong)', session['username'])
                return redirect(url_for("userrouting.changePassword"))
            if changepass_errors:
                flash(str(changepass_errors), category="error")
                app.logger.error('%s did not successfully change password (New passwords did not match)', session['username'])
                return redirect(url_for("userrouting.changePassword"))
            if current_password_check and not changepass_errors:
                newpassword = p.hash_password(newpassword)
                user_changePassword_db = db.changePassword_db(newpassword, session['username'])
                flash("Successfully changed password", category="success")
                app.logger.info('%s successfully changed password', session['username'])
                return redirect(url_for('userrouting.changePassword'))
        return render_template("user/changePassword.html", userid=session['userid'])
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))

###### user logout #####

def logout():
    try:
        if session.get('admin_name'):
            app.logger.info('Admin %s successfully logged out', session['admin_name'])
        else:
            app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("You have successfully logout.",category="success")
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))

###### user home or main page #####
@loginauth_required
def home():
    try:
        ##user home page db here
        dbresult = db.home_db()
        account = dbresult["account"]
        announcement = dbresult["announcement"]
        announc = dbresult["announc"]
        return render_template("user/home.html",account = account, announcement=announcement,announc=announc)
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))


###### web page about us information #####
@loginauth_required
def aboutus():
    try:
        ##user about us db here
        about_us_db = db.aboutUs_db()
        return render_template("about_us/aboutus.html",account=about_us_db)
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('%s successfully logged out', session['username'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))    


###### route for the static folder #####
def static_dir(path):
    return send_from_directory("static", path)
