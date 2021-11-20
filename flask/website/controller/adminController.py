from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask,session,send_from_directory
from website.controller.securityController import *
import website.model.admin_db as db
from .passwordController import PasswordController
import MySQLdb
adminauth = Blueprint('adminController', __name__,template_folder='views')
app = Flask(__name__,static_url_path='/static')


###### admin login #####
def adminLogin():
    try:
        if request.method == "POST":
            admin_name = validate_allow_symbols(request.form['admin_name'], "-_")
            admin_password = request.form['admin_password']
            p = PasswordController()
            if p.check_password(admin_password):
                flash(str(p.get_error_message()), category="error")
                app.logger.error('Admin %s failed to login', admin_name)
                return redirect(url_for('adminrouting.adminHome'))
            ##admin login db here
            retrieved_info = db.admin_login_db(str(admin_name))
            if retrieved_info:
                if p.verify_hash(admin_password, retrieved_info[2]):
                    session['adminLoggedIn'] = True
                    session['admin_name'] = retrieved_info[1]
                    session['admin_id'] = retrieved_info[0]
                    flash("You have successfully logged in.", category="success")
                    app.logger.info('Admin %s successfully logged in', admin_name)
                    return redirect(url_for('adminrouting.adminHome'))
            session['adminLoggedIn'] = False
            flash("Incorrect username or password", category="error")
            app.logger.error('Admin %s failed to login', admin_name)
            return redirect(url_for('adminrouting.adminLogin'))
        return render_template("admin/adminLogin.html")
    except MySQLdb.Error as ex:
        flash("Database error occured", category="error")  
        app.logger.error(ex)
        return redirect(url_for('adminrouting.adminLogin'))    
    except Exception as ex:
        flash("Unknown exception occured", category="error")
        app.logger.error(ex)
        return redirect(url_for('adminrouting.adminLogin'))   


###### display of admin profile information #####
@adminloginauth_required
def adminProfile():
    try:
        ##admin profile db here
        db.admin_profile_db()
        return render_template("admin/adminProfile.html",adminAccount=db.admin_profile_db())
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))    


###### admin home or main page #####
@adminloginauth_required
def adminHome():
    try:
        ##admin home db here
        dbresult = db.admin_home_db()
        adminAccount = dbresult["adminAccount"]
        announcement = dbresult["announcement"]
        announc = dbresult["announc"]
        return render_template("admin/adminHome.html",adminAccount=adminAccount,announcement=announcement,announc=announc)
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))
 

### admin about us ###
@adminloginauth_required
def adminaboutus():
    try:
        db.admin_about_us_db()
        return render_template("about_us/adminaboutus.html")
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('userrouting.login'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('userrouting.login'))

