from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask,session,send_from_directory
from website.controller.securityController import *
from website.forms.announcementform import AnnouncementForm
import website.model.adminForum_db as db
from .checkController import Check
import MySQLdb
import math
AForum = Blueprint('adminforuController', __name__,template_folder='views')
app = Flask(__name__,static_url_path='/static')
limit = 5
#### admin viewing of thread
@adminloginauth_required
def admin_view_thread(page: str = 1):
    try:
        #Getting number of pages
        #Add error checking for empty or 0 thread
        if validate_number(page):
            NumOfThread = db.get_num_of_threads()
            if(validate_number(NumOfThread) != 0):
                totalpages = math.ceil(NumOfThread / limit)
                if validate_number(totalpages):
                    if int(totalpages)<int(page):
                        page = int(totalpages)
                        return redirect(url_for('adminforumrouting.admin_view_thread'))
                    elif int(page) < 1:
                        page = 1
            elif(validate_number(NumOfThread) == 0):
                totalpages = 1
            #Getting results from DB based on page
            page = int(page)
            offset = (page - 1) * limit
            if(offset < 0):
                offset = 0
            dbresult = db.admin_view_thread_db(offset,limit)
            account = dbresult["account"]
            allthread = dbresult["allthread"]
            post = dbresult["post"]
            return render_template("admin/adminThread.html",account=account, allthread=allthread,post=post,totalpages= totalpages, page= page)
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

##admin delete thread ###
@adminloginauth_required
def admin_delete_thread(threadid):
    try:
        if validate_number(threadid):
            db.admin_delete_thread_db(int(threadid))
        return redirect(url_for("adminforumrouting.admin_view_thread"))
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


#### admin viewing of post  ###
@adminloginauth_required
def admin_view_post(threadid,page: str = 1):
    try:
        if validate_number(threadid):
            if validate_number(page):
                NumOfPost = db.get_num_of_posts()
                if(validate_number(NumOfPost) != 0):
                    totalpages = math.ceil(NumOfPost / limit)
                    if validate_number(totalpages):
                        if int(totalpages)<int(page):
                            page = int(totalpages)
                            return redirect(url_for('adminforumrouting.admin_view_thread'))
                        elif int(page) < 1:
                            page = 1
                elif(validate_number(NumOfPost) == 0):
                    totalpages = 1
                #Getting results from DB based on page
                page = int(page)
                offset = (page - 1) * limit
                if(offset < 0):
                    offset = 0
                ###view db here
                dbresult = db.admin_view_all_post_db(int(threadid),offset,limit)
                account = dbresult["account"]
                threadzz = dbresult["threadzz"]
                post = dbresult["post"]
                if not threadzz:
                    return redirect(url_for("adminforumrouting.admin_view_thread"))
                return render_template("admin/thread.html",account=account, threadzz=threadzz, post=post, totalpages=totalpages,page=page)
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


#### admin delete of post ###
@adminloginauth_required
def admin_delete_post(postid):
    try:
        if validate_number(postid):
            db.admin_delete_post_db(postid)
        return redirect(url_for("adminforumrouting.admin_view_thread"))
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
        
    
#### admin new announcement page ####
@adminloginauth_required
def new_announcement():
    return render_template("admin/new_announcement.html",form=AnnouncementForm())

### admin creation of announecment button function #####
@adminloginauth_required
def create_announcement():
    try:
        form = AnnouncementForm(request.form)
        if not form.validate():
            return render_template("admin/new_announcement.html", form=form)
        body = validate_text(form.body.data)
        if body:
            db.admin_insert_announcement_db(body)
        else:
            flash("Only the following characters are allowed: .,?!", category="error")
        return redirect(url_for('adminrouting.adminHome'))
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


### admin view announcement
@adminloginauth_required
def view_announcements(page: str = 1):
    try:
        #Getting number of pages
        #Add error checking for empty or 0 comments
        #Getting results from DB based on page
        if validate_number(page):
            NumOfAnnounce = db.get_num_of_announcement()
            if(validate_number(NumOfAnnounce) != 0):
                totalpages = math.ceil(NumOfAnnounce / limit)
                if validate_number(totalpages):
                    if int(totalpages)<int(page):
                        page = int(totalpages)
                        return redirect(url_for('adminforumrouting.admin_view_thread'))
                    elif int(page) < 1:
                        page = 1
            elif(validate_number(NumOfAnnounce) == 0):
                totalpages = 1
            page = int(page)
            offset = (page - 1) * limit
            if(offset < 0):
                offset = 0
            dbresult = db.admin_view_announcement_db(offset,limit)
            account = dbresult["account"]
            announcements = dbresult["announcements"]
            return render_template("admin/announcement_list.html",account= account, announcements= announcements, totalpages= totalpages, page= page)
    except MySQLdb.Error as ex: 
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Database error occured, please log in again.", category="error") 
        return redirect(url_for('adminrouting.adminLogin'))
    except Exception as ex:
        app.logger.error(ex)
        app.logger.info('Admin %s successfully logged out', session['admin_name'])
        session.clear()
        flash("Unknown exception occured, please log in again", category="error")
        return redirect(url_for('adminrouting.adminLogin')) 


#### edit of announcement 
@adminloginauth_required
def admin_edit_announcement(announcementID):
    try:
        if validate_number(announcementID):
            test: int = Check.check_owner_announcement(int(announcementID), session.get("admin_id"))
            if test == 0:
                return redirect(url_for("adminforumrouting.view_announcements"))
            dbresult = db.admin_view_edit_announcement_db(int(announcementID))
            announcements = dbresult["announcements"]
            return render_template("admin/update_announcement.html",announcements=announcements)
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


#### update of announcement ###
@adminloginauth_required
def admin_update_announcement(announcementID):
    try:
        if request.method == "POST":
            body = validate_text(request.form['body'])
            if body and validate_number(announcementID):
                db.admin_update_announcement_db(body,int(announcementID))
            elif not body:
                flash("Only the following characters are allowed: .,?!", category="error")
            return redirect(url_for("adminforumrouting.view_announcements"))
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


### admin delete announcement ###
@adminloginauth_required
def admin_delete_announcement(announcementID):
    try:
        if validate_number(announcementID):
            db.admin_delete_announcement_db(int(announcementID))
            return redirect(url_for("adminforumrouting.view_announcements"))
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
