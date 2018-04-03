# -*- coding: utf-8 -*-

import string
from functools import wraps
from random import *

from flask import current_app, redirect, request, session, url_for

from web_frame.web_blueprint import web_frame
from web_frame.model import db
from web_frame.model.user import User
from web_frame.web_logger import Log

@web_frame.after_request
def add_header(r):
    """Disable page caching to avoid back-button problems"""
    
    r.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return r
 
@web_frame.teardown_request
def close_db_session(exception=None):
    
    try:
        db.session.remove()
    except Exception as e:
        Log.error(str(e))


########################################################################
def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Check whether logged in"""
        try:
            session_key = request.cookies.get(
                          current_app.config['SESSION_COOKIE_NAME'])
            is_login = False
            if session.sid == session_key and session.__contains__('user_info'):
                is_login = True
            
            if not is_login:
                return redirect(url_for('web_frame.login', next=request.url))
            
            return f(*args, **kwargs)
        
        except Exception as e:
            Log.error('Web error: %s' % str(e))
            raise e
            
    return decorated_function

def get_user(username):
    try:
        current_user = User.query.filter_by(username=username).first()
        Log.debug(current_user)
        return current_user
    
    except Exception as e:
        Log.error(str(e))
        raise e
        
def password_generator():
    characters = string.ascii_letters + string.digits
    password = ''.join(choice(characters) for x in range(randint(20,30)))
    return password
    