from flask import Blueprint
from website.controller.adminforumController import admin_view_post, admin_view_thread, create_announcement,new_announcement, view_announcements,admin_delete_announcement,admin_delete_thread,admin_delete_post,admin_update_announcement,admin_edit_announcement


adminforumrouting = Blueprint('adminforumrouting', __name__)

adminforumrouting.route("/admin_view_thread", methods=["GET"])(admin_view_thread)
adminforumrouting.route("/admin_view_thread/page/<page>", methods=["GET"])(admin_view_thread)
adminforumrouting.route("/admin_view_thread/<threadid>", methods=["GET"])(admin_view_post)
adminforumrouting.route("/admin_view_thread/<threadid>/page/<page>", methods=["GET"])(admin_view_post)
adminforumrouting.route('/new_announcement')(new_announcement)
adminforumrouting.route("/create_announcement", methods=["POST"])(create_announcement)
adminforumrouting.route("/view_announcements", methods=["GET"])(view_announcements)
adminforumrouting.route("/view_announcements/page/<page>", methods=["GET"])(view_announcements)
adminforumrouting.route("/view_announcements/edit/<announcementID>", methods=['GET','POST'])(admin_edit_announcement)
adminforumrouting.route("/view_announcements/update/<announcementID>", methods=["POST"])(admin_update_announcement)
adminforumrouting.route("/view_announcements/delete/<announcementID>", methods=['GET', 'POST'])(admin_delete_announcement)
adminforumrouting.route("/admin_view_thread/delete/<threadid>", methods=['GET', 'POST'])(admin_delete_thread)
adminforumrouting.route("/admin_view_thread/deletepost/<postid>", methods=['GET', 'POST'])(admin_delete_post)