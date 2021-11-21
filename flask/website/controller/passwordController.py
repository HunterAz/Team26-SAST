#!usr/bin/python3
import os 
import gzip
import re
from .securityController import *
from passlib.hash import pbkdf2_sha256

class PasswordController():
    def __init__(self):
        self.error_message = ""
        self.ALLOWED_CHARS = "!?()[]+-_^"
        self.PASSWORD_LIST_PATH = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "static", "5k_common_pass.txt.gz")
    
    def __str__(self):
        return self.error_message

    def get_error_message(self):
        return self.error_message

    def set_error_message(self, e):
        self.error_message += e
        self.error_message += ","

    def get_allowed_chars(self):
        return self.ALLOWED_CHARS

    def check_common_password(self, passwd):
        """
        Check given password from a list of common 5000 passwords to check for a match
        List was taken from the old rockyou.txt
        """
        try:
            common_pw_list = gzip.open(self.PASSWORD_LIST_PATH).read().decode('utf-8').splitlines()
        except Exception:
            with open(self.PASSWORD_LIST_PATH) as f:
                common_pw_list = f.readlines()
        if passwd in common_pw_list:
            self.set_error_message("Password is too common")

    def check_complex_password(self, passwd):
        if len(passwd) < 8:
            self.set_error_message("Password should be more than 8 characters")
        if len(passwd) > 64:
            self.set_error_message("Password should be lesser than 64 characters")
        if passwd.isdigit():
            self.set_error_message("Password should not be all numbers")
        if re.findall(r'((\w)\2{2,})', passwd):
            self.set_error_message("Password has consecutive repeating characters more than 2 times")
    
    def check_password_symbols(self, passwd):
        if validate_allow_symbols(passwd, self.get_allowed_chars()) is None:
            self.set_error_message("Only the following characters are allowed in passwords: %s" % self.get_allowed_chars())

    def hash_password(self, passwd):
        return pbkdf2_sha256.hash(passwd)

    def verify_hash(self, user_hash, stored_hash):
        return pbkdf2_sha256.verify(user_hash, stored_hash)

    def check_password(self,passwd, cfmpasswd=None):
        self.check_common_password(passwd)
        self.check_complex_password(passwd)
        self.check_password_symbols(passwd)
        if cfmpasswd and passwd != cfmpasswd:
            self.set_error_message("Password fields do not match")
        if self.get_error_message():
            return self.get_error_message()

