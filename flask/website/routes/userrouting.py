from flask import Blueprint, Flask
from website.controller.userController import aboutus, changePassword,forgetPassword, home, login, logout, newPassword, profile, sign_up, static_dir, update, verify, unconfirmed, confirmation, resend_confirmation


userrouting = Blueprint('userrouting', __name__)

userrouting.route('/sign_up', methods=['GET', 'POST'])(sign_up)
userrouting.route('/login', methods=['GET', 'POST'])(login)
userrouting.route('/profile', methods=['GET', 'POST'])(profile)
userrouting.route('/update', methods=['GET', 'POST'])(update)
userrouting.route('/forgetPassword', methods=['GET', 'POST'])(forgetPassword)
userrouting.route('/newPassword/<token>', methods=['GET', 'POST'])(newPassword)
userrouting.route('/changePassword', methods=['GET', 'POST'])(changePassword)
userrouting.route('/verify', methods = ['GET', 'POST'])(verify)
userrouting.route('/unconfirmed')(unconfirmed)
userrouting.route('/confirmation/<token>')(confirmation)
userrouting.route('/resend_confirmation')(resend_confirmation)
userrouting.route('/logout')(logout)
userrouting.route('/home')(home)
userrouting.route('/aboutus')(aboutus)
userrouting.route("/static/<path:path>")(static_dir)
