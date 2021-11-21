from flask import Blueprint
from website.controller.userforumController import  create_post,view_thread, delete_post,edit_post,update_post,all_thread, create_thread, new_thread, delete_thread, edit_thread,update_thread


forumrouting = Blueprint('forumrouting', __name__)

forumrouting.route('/new_thread')(new_thread)
forumrouting.route("/create_thread", methods=["POST"])(create_thread)
forumrouting.route("/all_thread", methods=["GET"])(all_thread)
forumrouting.route("/all_thread/page/<page>", methods=["GET"])(all_thread)
forumrouting.route("/all_thread/<threadid>", methods=["GET"])(view_thread)
forumrouting.route("/all_thread/<threadid>/page/<page>", methods=["GET"])(view_thread)
forumrouting.route("/all_thread/<threadid>/posts", methods=["POST"])(create_post)
forumrouting.route("/all_thread/edit/<threadid>", methods=['GET'])(edit_thread)
forumrouting.route("/all_thread/updatethread/<threadid>", methods=["POST"])(update_thread)
forumrouting.route("/all_thread/editpost/<postid>", methods=["GET"])(edit_post)
forumrouting.route("/all_thread/updatepost/<postid>", methods=["POST"])(update_post)
forumrouting.route("/all_thread/delete/<threadid>", methods=['GET', 'POST'])(delete_thread)
forumrouting.route("/all_thread/deletepost/<postid>", methods=['GET', 'POST'])(delete_post)