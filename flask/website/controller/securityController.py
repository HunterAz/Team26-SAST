from functools import wraps

from flask import  redirect, url_for, session, flash
import string
import re

def loginauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userid") is None:
            return redirect(url_for("userrouting.login"))
        elif str(session.get("verified")) == "0":
            flash(session.get("verified"), 'success')
            return redirect(url_for("userrouting.unconfirmed"))
        elif session.get("verified") is None:
            return redirect(url_for("userrouting.login"))
        elif session.get("loggedIn") is True:
            if str(session.get("verified")) == "1":
                if str(session.get('locked')) == "1":
                    return redirect(url_for("userrouting.verify"))
        return f(*args, **kwargs)
    return decorated_function

def loginpage_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('loggedIn') is True:
            if str(session.get('verified') == "0"):
                return redirect(url_for("userrouting.unconfirmed"))
            return redirect(url_for("userrouting.home"))
        return f(*args, **kwargs)

    return decorated_function

def verify_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('loggedIn') is True:
            pass
        else:
            return redirect(url_for("userrouting.login"))
        return f(*args, **kwargs)

    return decorated_function

def adminloginauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect(url_for("userrouting.login"))
        return f(*args, **kwargs)

    return decorated_function

def validate_text(text):
    allowed = set(string.ascii_letters + string.digits + " .,?!")
    for char in text:
        if not (char in allowed):
            return None
    return text

def validate_allow_symbols(text, allow=""):
    allowed = set(string.ascii_letters + string.digits + allow)
    for char in text:
        if not (char in allowed):
            return None
    return text

def validate_date(date):
    allowed = string.digits + "-"
    sd = ''.join(char for char in date if char in allowed)
    valid_date_rgx = '^\d{4}-\d{2}-\d{2}$'
    if re.search(valid_date_rgx, sd):
        return sd
    else:
        return None

def validate_email(email):
    s = validate_allow_symbols(email, ".@")
    valid_email_rgx = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(valid_email_rgx, s):
        return s
    else:
        return None

def validate_number(n):
    try:
        return int(n)
    except ValueError:
        return None

