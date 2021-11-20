import website.model.userForum_db as db
import website.model.adminForum_db as db1
class Check:
    @staticmethod
    def check_owner_thread(threadid: str, user_id: str) -> int:
        ret: db = db.check_user_thread(threadid, user_id)
        return 0 if ret is None else 1

    @staticmethod
    def check_owner_post(postid: str, user_id: str) -> int:
        ret: db = db.check_user_post(postid, user_id)
        return 0 if ret is None else 1

    @staticmethod
    def check_owner_announcement(annnouncementid: str, user_id: str) -> int:
        ret: db1 = db1.check_admin_announcemnt(annnouncementid, user_id)
        return 0 if ret is None else 1