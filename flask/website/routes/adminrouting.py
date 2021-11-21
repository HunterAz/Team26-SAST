from flask import Blueprint
from website.controller.adminController import adminHome, adminLogin, adminProfile, adminaboutus


adminrouting = Blueprint('adminrouting', __name__)

adminrouting.route('/adminLogin', methods=['GET', 'POST'])(adminLogin)
adminrouting.route('/adminProfile', methods=['GET', 'POST'])(adminProfile)
adminrouting.route('/adminHome')(adminHome)
adminrouting.route('/adminaboutus')(adminaboutus)