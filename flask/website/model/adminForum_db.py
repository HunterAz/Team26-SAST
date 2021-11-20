from flask_mysqldb import MySQL
from datetime import timedelta , datetime
from flask import flash,Flask,session,request
import MySQLdb

app = Flask(__name__)
mysql = MySQL(app)
## admin viewing of thread database ##

def admin_view_thread_db(offset, limit):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    account = cursor.fetchone()
    cursor.execute("SELECT *, User.username, User.user_id FROM Thread INNER JOIN User ON User.user_id = Thread.user_id ORDER BY threadid DESC LIMIT %s, %s",[offset,limit])
    allthread = cursor.fetchall()
    cursor.execute("SELECT threadid, COUNT(*) As NUM FROM Post group by threadid" )
    post = cursor.fetchall()
    cursor.close()
    returndata = {
        'account':account,
        'allthread':allthread,
        'post':post
    }
    return returndata

## admin deleting of thread database ##

def admin_delete_thread_db(threadid):
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

### post start from here ###

## admin viewing all the post database ##

def admin_view_all_post_db(threadid,offset,limit):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
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

## admin deleting post database ##

def admin_delete_post_db(postid):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("DELETE Post FROM Post WHERE Post.post_id = %s",[postid])
    mysql.connection.commit()
    cursor.close()
    return postid


### announcement start from here ###

## admin creating announcement database ##

def admin_insert_announcement_db(body):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    account = cursor.fetchone()
    author_id = account['Adminid']
    cursor.execute("INSERT INTO Announcement(announcement_details,adminid, announcement_date, announcement_editdate) VALUES (%s,%s,CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore'),CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore'))",
                    (body, author_id))
    mysql.connection.commit()
    cursor.close()
    return body,author_id

## admin viewing all announcement database ##

def admin_view_announcement_db(offset, limit):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    account = cursor.fetchone()
    cursor.execute("SELECT * from Announcement ORDER BY announcementID DESC LIMIT %s, %s",[offset,limit])
    announcements = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    returndata = {
        'account':account,
        'announcements':announcements
    }
    return returndata

## admin viewing the announcement they want to edit database ##

def admin_view_edit_announcement_db(announcementID):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    account = cursor.fetchone()
    cursor.execute("SELECT * FROM Announcement WHERE announcementID = %s ",[announcementID])
    announcements = cursor.fetchone()
    returndata = {
        'account':account,
        'announcements':announcements
    }
    return returndata

## admin update / edit the announcement database ##

def admin_update_announcement_db(body,announcementID):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("UPDATE Announcement SET announcement_details= %s,announcement_date=CONVERT_TZ(NOW(),'SYSTEM','Asia/Singapore') where announcementID = %s ", [body,announcementID])
    mysql.connection.commit()
    cursor.close()
    return body,announcementID

## admin delete the announcement database ##

def admin_delete_announcement_db(announcementID):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("DELETE Announcement FROM Announcement WHERE Announcement.announcementID = %s",[announcementID])
    mysql.connection.commit()
    cursor.close()
    return announcementID

## checking owner of announcement database ##
def check_admin_announcemnt(announcementID, admin_id):
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT announcement_details FROM Announcement Where announcementID = %s AND adminid = %s",[announcementID,admin_id])
    cursor = cursor.fetchone()
    return cursor

## checking number of announcement database ##
def get_num_of_announcement():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT COUNT(announcementID) AS number FROM Announcement")
    cursor = cursor.fetchone()
    return cursor["number"]

## checking number of thread database ##
def get_num_of_threads():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT COUNT(threadid) AS number FROM Thread")
    cursor = cursor.fetchone()
    return cursor["number"]

## checking number of post database ##
def get_num_of_posts():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT COUNT(post_id) AS number FROM Post")
    cursor = cursor.fetchone()
    return cursor["number"]