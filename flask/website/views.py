from flask import Blueprint, render_template

views = Blueprint('views',__name__,template_folder='views')

@views.route('/')
def login():
    return render_template("user/login.html")