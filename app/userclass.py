from flask_login import UserMixin
from flask_login._compat import unicode



class DbUser(object):
    """Wraps User object for Flask-Login"""
    user=None
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return unicode(self.user.userid)

    def is_active(self):
        return self.user.enabled

    def get_user(self):
        return self.user

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True