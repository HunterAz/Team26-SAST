from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask,session,send_from_directory
from website.forms.threadform import ThreadForm
from website.forms.postform import PostForm
import website.model.userForum_db as db
from .checkController import Check
from .securityController import *
import MySQLdb
import math

limit = 5
userforum = Blueprint('userforumController', __name__,template_folder='views')
app = Flask(__name__,static_url_path='/static')

###### all thread #####
@loginauth_required
def all_thread(page: str = 1):
    try:
        #Getting number of pages
        #Add error checking for empty or 0 thread
        if validate_number(page):
            NumOfThread = db.get_num_of_userthreads()
            if(validate_number(NumOfThread) != 0):
                totalpages = math.ceil(NumOfThread / limit)
                if validate_number(totalpages):
                    if int(totalpages)<int(page):
                        page = int(totalpages)
                        return redirect(url_for('forumrouting.all_thread'))
                    elif int(page) < 1:
                        page = 1
            elif(validate_number(NumOfThread) == 0):
                totalpages = 1
            #Getting results from DB based on page
            page = int(page)
            offset = (page - 1) * limit
            if(offset < 0):
                offset = 0
            dbresult = db.user_all_thread_db(offset,limit)
            useracc = dbresult["useracc"]
            useracc = useracc['user_id']
            allthread = dbresult["allthread"]
            post = dbresult["post"]
            return render_template("thread/all_thread.html", useracc=useracc, allthread=allthread,post=post,totalpages= totalpages, page= page)
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

###### display of new thread page #####
@loginauth_required
def new_thread():
    return render_template("thread/new_thread.html", form=ThreadForm())

###### creation of thread #####
@loginauth_required
def create_thread():
    try:
        ##create thread here
        form = ThreadForm(request.form)
        if not form.validate():
            return render_template("thread/new_thread.html", form=form)
        subject = validate_text(form.subject.data)
        body = validate_text(form.body.data)
        if not subject or not body:
            flash("Only the following characters are allowed: .,?!", category="error")
            return render_template("thread/new_thread.html", form=form)
        if subject and body:
            ##insert create thread here
            db.insert_create_thread_db(subject,body)
        return redirect(url_for("forumrouting.all_thread"))
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

## user delete thread
@loginauth_required
def delete_thread(threadid):
    try:
        if validate_number(threadid):
            test: int = Check.check_owner_thread(int(threadid), session.get("userid"))
            if test != 0:
                #user delete thread db here
                db.user_delete_thread_db(int(threadid))
        return redirect(url_for("forumrouting.all_thread"))
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

## user view of edit thread
@loginauth_required
def edit_thread(threadid):
    try:
        if validate_number(threadid):
            test: int = Check.check_owner_thread(int(threadid), session.get("userid"))
            if test != 0:
                dbresult = db.user_view_edit_thread_db(int(threadid))
                thread = dbresult["thread"]
                return render_template("thread/editthread.html",thread=thread)
        ##user view edit thread db here
        return redirect(url_for("forumrouting.all_thread"))
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

## user update / edit of that thread
@loginauth_required
def update_thread(threadid):
    try:
        if request.method == "POST":
            if validate_number(threadid):
                test: int = Check.check_owner_thread(int(threadid), session.get("userid"))
                editsubject = validate_text(request.form['editsubject'])
                editbody = validate_text(request.form['editbody'])
                if not editsubject or not editbody:
                    flash("Only the following characters are allowed: .,?!", category="error")
                if test != 0 and editsubject and editbody:
                    ##user edit thread db here
                    db.user_edit_thread_db(editsubject, editbody,threadid)
            return redirect(url_for("forumrouting.all_thread"))
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


### view all the thread ####
@loginauth_required
def view_thread(threadid, page: str = 1):
    try:
        if validate_number(threadid):
            #Getting number of pages
            #Add error checking for empty or 0 thread
            if validate_number(page):
                NumOfPost = db.get_num_of_userpost()
                if(validate_number(NumOfPost) != 0):
                    totalpages = math.ceil(NumOfPost / limit)
                    if validate_number(totalpages):
                        if int(totalpages)<int(page):
                            page = int(totalpages)
                            return redirect(url_for('forumrouting.all_thread'))
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
                dbresult = db.viewing_of_thread_db(int(threadid),offset,limit)
                account = dbresult["account"]
                account = account['user_id']
                threadzz = dbresult["threadzz"]
                post = dbresult["post"]
                if not threadzz:
                    return redirect(url_for("forumrouting.all_thread"))
                return render_template("thread/thread.html", account=account, threadzz=threadzz, post=post,form=PostForm(),totalpages=totalpages,page=page)
        return redirect(url_for("forumrouting.all_thread"))
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

#### creation of post ###
@loginauth_required
def create_post(threadid):
    try:
        form = PostForm(request.form)
        if not form.validate():
            return render_template("thread/thread.html", form=form)
        body = validate_text(form.body.data)
        if body and validate_number(threadid):
            ##user create post db here
            db.user_insert_of_post_db(body, int(threadid))
        else:
            flash("Only the following characters are allowed: .,?!", category="error")
        return redirect(url_for("forumrouting.all_thread"))
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


#### delete of post
@loginauth_required
def delete_post(postid):
    try:
        if validate_number(postid):
            test: int = Check.check_owner_post(int(postid), session.get("userid"))
            if test != 0:
                #user delete post db here
                db.user_delete_post_db(int(postid))
        return redirect(url_for("forumrouting.all_thread"))
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

#### edit of post 
@loginauth_required
def edit_post(postid):
    try:
        if validate_number(postid):
            test: int = Check.check_owner_post(int(postid), session.get("userid"))
            if test != 0:
                dbresult = db.user_view_edit_post_db(int(postid))
                post = dbresult["post"]
                return render_template("post/editpost.html",post=post)
        return redirect(url_for("forumrouting.all_thread"))
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


#### update of post 
@loginauth_required
def update_post(postid):
    try:
        if request.method == "POST":
            if validate_number(postid):
                editbody = validate_text(request.form['editbody'])
                test: int = Check.check_owner_post(int(postid), session.get("userid"))
                if test != 0 and editbody:
                    ##user edit post db here
                    db.user_edit_post_db(editbody,int(postid))
                if not editbody:
                    flash("Only the following characters are allowed: .,?!", category="error")
            return redirect(url_for("forumrouting.all_thread"))
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
