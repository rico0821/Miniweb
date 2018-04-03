# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, url_for


def print_settings(config):
    print('-----------------------------------------------')
    print('SETTINGS')
    print('-----------------------------------------------')
    for key, value in config:
        print('%s=%s' % (key, value))
    print('-----------------------------------------------')

############################################################################
def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500

############################################################################
def create_app(config_filepath='resource/config.cfg'):
    
    web_app = Flask(__name__)
        
    #CONFIG
    from web_frame.web_config import webConfig
    web_app.config.from_object(webConfig)
    web_app.config.from_pyfile(config_filepath, silent=True)
    print_settings(web_app.config.items())
    
    #Initialise Log
    from web_frame.web_logger import Log
    log_filepath = os.path.join(web_app.root_path,
                                web_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)
    
    #Load DB, Migrate
    from flask_migrate import Migrate
    from web_frame.model import db
    db.init_app(web_app)
    migrate = Migrate(web_app, db)
      
    #Model
    from web_frame.model.user import User
    with web_app.app_context():
        db.create_all() # Create tables
    
    #Admin
    from flask_admin import Admin
    from web_frame.admin import AdminLogin, AuthModelView
    admin = Admin(web_app, index_view=AdminLogin(), name='miniweb', template_mode='bootstrap3')
    admin.add_view(AuthModelView(User, db.session))
    
    #Mail
    from web_frame.web_mail import mail
    mail.init_app(web_app)
    
    #Load view functions
    from web_frame.controller import general
    from web_frame.controller import login
    from web_frame.controller import register_user
    from web_frame.controller import main
    from web_frame.controller import email
    from web_frame.controller import recover
    
    #Blueprint
    from web_frame.web_blueprint import web_frame 
    web_app.register_blueprint(web_frame)
        
    #SessionInterface
    from web_frame.cache_session import SimpleCacheSessionInterface
    web_app.session_interface = SimpleCacheSessionInterface()
    
    #Common error handlers
    web_app.register_error_handler(404, not_found)
    web_app.register_error_handler(500, server_error)
    
    return web_app
    

    