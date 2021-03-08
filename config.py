import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'postgres://pafohykylwfsvl:0b0dae8f00a068dd9ea854638782c6c472a01ed03907ae3296d1fe6e976f1c27@ec2-54-242-43-231.compute-1.amazonaws.com:5432/dcc9306sv3fdi2'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
