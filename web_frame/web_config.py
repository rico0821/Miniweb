# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class webConfig:
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'resource/database', 'web.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    TEMP_FOLDER= 'resource/temp/'
    # Session
    PERMANENT_SESSION_LIFETIME = 60 * 60
    SESSION_COOKIE_NAME= 'web_session'
    # Log
    LOG_LEVEL= 'debug'
    LOG_FILE_PATH= 'resource/log/web.log'
    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = 'example@gmail.com'
    MAIL_USERNAME = 'example@gmail.com'
    MAIL_PASSWORD = 'example'
    TESTING = True

    