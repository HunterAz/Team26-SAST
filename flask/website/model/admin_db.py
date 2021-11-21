from flask_mysqldb import MySQL
from datetime import timedelta , datetime
from flask import flash,Flask,session,request
import MySQLdb

app = Flask(__name__)
mysql = MySQL(app)
## admin login database ##

def admin_login_db(admin_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Admin where admin_name = %s", [admin_name])
    adminAccount = cursor.fetchone()
    cursor.close()
    return adminAccount

## admin viewing their profile database ##

def admin_profile_db():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    adminAccount = cursor.fetchone()
    cursor.close()
    return adminAccount

## admin home page database ##

def admin_home_db():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    adminAccount = cursor.fetchone()
    cursor.execute("SELECT * from Announcement")
    announcement = cursor.fetchall()
    cursor.execute("SELECT * from Announcement ORDER BY announcementID DESC LIMIT 1")
    announc = cursor.fetchone()
    cursor.close()
    returndata = {
        'adminAccount':adminAccount,
        'announcement':announcement,
        'announc': announc
    }
    return returndata


## admin about us page database ##

def admin_about_us_db():
    cursor = mysql.connection.cursor((MySQLdb.cursors.DictCursor))
    cursor.execute("SELECT * from Admin where Adminid = %s ", [session['admin_id']])
    account = cursor.fetchone()
    cursor.close()
    return account