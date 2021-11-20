from flask_mysqldb import MySQL
from datetime import timedelta , datetime
from flask import flash,Flask,session,request
import MySQLdb

app = Flask(__name__)
mysql = MySQL(app)

## user create of thread database ##

def insert_create_thread_db(subject,body):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    account = cursor.fetchone()
    mainrouteor_id = account['user_id']
    cursor.execute("INSERT INTO Thread(thread_title,thread_details,thread_date,thread_editdate,user_id) VALUES (%s,%s,CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore'),CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore'),%s)",
                    (subject, body, mainrouteor_id))
    mysql.connection.commit()
    cursor.close()
    return subject,body,mainrouteor_id

## user viewing all threads database ##

def user_all_thread_db(offset,limit):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    useracc = cursor.fetchone()
    cursor.execute("SELECT  * FROM Thread INNER JOIN User ON User.user_id = Thread.user_id ORDER BY threadid DESC LIMIT %s, %s",[offset,limit])
    allthread = cursor.fetchall()
    cursor.execute("SELECT threadid, COUNT(*) As NUM FROM Post group by threadid" )
    post = cursor.fetchall()
    cursor.close()
    returndata = {
        'useracc':useracc,
        'allthread':allthread,
        'post':post
    }
    return returndata

def get_num_of_userthreads():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT COUNT(threadid) AS number FROM Thread")
    cursor = cursor.fetchone()
    return cursor["number"]

## checking user details of thread from database ##
def check_user_thread(threadid, user_id):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT thread_title FROM Thread Where threadid = %s AND user_id = %s",[threadid,user_id])
    cursor = cursor.fetchone()
    return cursor


## user viewing of that thread details they want to edit database ##

def user_view_edit_thread_db(threadid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    useracc = cursor.fetchone()
    cursor.execute("SELECT  * FROM Thread INNER JOIN User ON User.user_id = Thread.user_id WHERE Thread.threadid = %s ",[threadid])
    thread = cursor.fetchone()
    returndata = {
        'useracc':useracc,
        'thread':thread
    }
    return returndata

## user updating / editing of that thread database ##

def user_edit_thread_db(editsubject, editbody,threadid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE Thread SET thread_title=%s,thread_details= %s,thread_editdate=CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore') WHERE Threadid=%s",[editsubject,editbody,threadid])
    mysql.connection.commit()
    cursor.close()
    return editsubject, editbody,threadid

## user deleting of that thread database ##

def user_delete_thread_db(threadid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * FROM Post INNER JOIN User ON User.user_id = Post.user_id INNER JOIN Thread ON Post.threadid = Thread.threadid WHERE Thread.threadid = %s",[threadid] )
    post = cursor.fetchall()
    if len(post) != 0:
        cursor.execute("DELETE Post,Thread FROM Thread INNER JOIN Post ON Thread.threadid = Post.threadid WHERE Thread.threadid = %s",[threadid])
        mysql.connection.commit()
        cursor.close()
    else:
        cursor.execute("DELETE Thread FROM Thread WHERE Thread.threadid = %s",[threadid])
        mysql.connection.commit()
        cursor.close()
    return threadid

## user viewing of the post inside the thread database ##

def viewing_of_thread_db(threadid, offset,limit):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    account = cursor.fetchone()
    cursor.execute("SELECT *, User.username, User.user_id FROM Thread INNER JOIN User ON User.user_id = Thread.user_id WHERE Thread.threadid = %s",[threadid])
    threadzz = cursor.fetchone()
    cursor.execute("SELECT * FROM Post INNER JOIN User ON User.user_id = Post.user_id INNER JOIN Thread ON Post.threadid = Thread.threadid WHERE Thread.threadid = %s ORDER BY post_id DESC LIMIT %s, %s",[threadid,offset,limit])
    post = cursor.fetchall()
    cursor.close()
    returndata = {
        'account':account,
        'threadzz':threadzz,
        'post': post
    }
    return returndata

### post start from here ###

## checking user details of post from database ##
def check_user_post(postid, user_id):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT post_details FROM Post Where post_id = %s AND user_id = %s",[postid,user_id])
    cursor = cursor.fetchone()
    return cursor


def get_num_of_userpost():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT COUNT(post_id) AS number FROM Post")
    cursor = cursor.fetchone()
    return cursor["number"]


## user creating post database ##

def user_insert_of_post_db(body,threadid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    account = cursor.fetchone()
    mainrouteor_id = account['user_id']
    cursor.execute("INSERT INTO Post(post_details,threadid,post_date,post_editdate,user_id) VALUES (%s,%s,CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore'),CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore'),%s)",
                    (body, threadid,mainrouteor_id))
    mysql.connection.commit()
    cursor.close()
    return body, threadid,mainrouteor_id

## user deleting of post database ##

def user_delete_post_db(postid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("DELETE Post FROM Post WHERE Post.post_id = %s",[postid])
    mysql.connection.commit()
    cursor.close()
    return postid

## user viewing of the post they want to edit database ##

def user_view_edit_post_db(postid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from User where user_id = %s ", [session['userid']])
    useracc = cursor.fetchone()
    cursor.execute("SELECT * FROM Post INNER JOIN Thread ON Post.threadid = Thread.threadid WHERE Post.post_id=%s",[postid])
    post = cursor.fetchone()
    returndata = {
        'useracc':useracc,
        'post':post
    }
    return returndata

## user updating / editing the post database ##

def user_edit_post_db(editbody,postid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE Post SET post_details= %s,post_editdate=CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore') WHERE post_id=%s",[editbody,postid])
    mysql.connection.commit()
    cursor.close()
    return editbody,postid