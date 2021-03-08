from flask import Flask
from flask_login import LoginManager
import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


# Initialization
application = Flask(__name__)
application.config.from_object(config.Config)



DB_URI = application.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)





# from .auth import auth as auth_blueprint
# application.register_blueprint(auth_blueprint)
#
#     # blueprint for non-auth parts of app
# from .main import main as main_blueprint
# application.register_blueprint(main_blueprint)
