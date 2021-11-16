from flask_mysqldb import MySQL
from flask import flash,Flask,session,request
from datetime import timedelta, datetime
import MySQLdb

app = Flask(__name__)
mysql = MySQL(app)

def sign_up_db(email,username,password,dob,verification_key):
    cursor = mysql.connection.cursor()
    current_date = datetime.now()
    cursor.execute("INSERT INTO User(email,username,password,dob,verification_key,verified,verified_datetime,otp,otp_lock,lockout_counter) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (email, username, password, dob, verification_key, '0', current_date, '000000', '0', '0'))
    mysql.connection.commit()
    cursor.close()
    flash("Account successfully created", category="success")
    return email,username,password,dob

def clear_verification(username):
    verification_key = None
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET verification_key  = %s where username = %s", (verification_key, username))
    mysql.connection.commit()
    cursor.close()
    return username

def verification_update(username, verification_key):
    current_date = datetime.now()
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET verification_key  = %s where username = %s", (verification_key, username))
    cursor.execute("UPDATE User SET verified_datetime  = %s where username = %s", (current_date, username))
    mysql.connection.commit()
    cursor.close()
    return verification_key

def get_user_verification_db(token):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from User where verification_key = %s", [token])
    account = cursor.fetchone()
    cursor.close()
    return account

#Store OTP value
def store_otp(username, otp):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET otp = %s where username = %s", [otp, username])
    mysql.connection.commit()
    cursor.close()
    return username

#Enable account lockout if OTP tries more than 3
def enable_otp_lock(username):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET otp_lock = 1 where username = %s", [username])
    mysql.connection.commit()
    cursor.close()
    return username

#Increment count of account lockout counter    
def update_account_lock(username):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET lockout_counter = lockout_counter + 1 where username = %s", [username])
    mysql.connection.commit()
    cursor.close()
    return username

#Reset account lockout counter once successfully login    
def reset_account_lock(username):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET lockout_counter = 0 where username = %s", [username])
    mysql.connection.commit()
    cursor.close()
    return username

## user update verification status ##
def verification(username):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    verified = 1
    cursor.execute("UPDATE User SET verified  = %s where username = %s", (verified, username))
    mysql.connection.commit()
    cursor.close()
    return verified
## user login database ##

def login_db(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from User where username = %s", [username])
    account = cursor.fetchone()
    cursor.close()
    return account

def email_db(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from User where email = %s", [email])
    account = cursor.fetchone()
    cursor.close()
    return account

## user profile database ##

def profile_db():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    account = cursor.fetchone()
    cursor.close()
    return account

## user update of profile database ##

def update_db(bios):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE User SET bios = %s where user_id = %s ", (bios, [session['userid']]))
    mysql.connection.commit()
    cursor.close()
    flash("You have successfully updated your profile.",category="success")
    return bios

def newPassword_db(password, email):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE User SET password= %s where email = %s ", (password,email))
    mysql.connection.commit()
    cursor.close()
    flash("Successfully updated your password", category="success")
    return password

def changePassword_db(newpassword, username):
    #cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE User SET password= %s where username = %s ", (newpassword,username))
    mysql.connection.commit()
    cursor.close()
    return newpassword

## home page database ##

def home_db():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    account = cursor.fetchone()
    cursor.execute("SELECT * from Announcement")
    announcement = cursor.fetchall()
    cursor.execute("SELECT * from Announcement ORDER BY announcementID DESC LIMIT 1")
    announc = cursor.fetchone()
    cursor.close()
    returndata = {
        'account':account,
        'announcement':announcement,
        'announc': announc
    }
    return returndata

## user about us database ##

def aboutUs_db():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    account = cursor.fetchone()
    cursor.close()
    return account
