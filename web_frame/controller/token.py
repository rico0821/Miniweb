# -*- coding: utf-8 -*-

from flask import abort, redirect, render_template, request, session, url_for
from itsdangerous import URLSafeTimedSerializer, BadSignature

from web_frame.web_blueprint import web_frame
from web_frame.web_logger import Log
from web_frame.model import db
from web_frame.model.user import User


@web_frame.route('/user/activate/<token>')
def activate_user(token):
    
    try:
        email = confirm_token(token)
        print(email)
        
    except BadSignature:
        Log.error(str(BadSignature))
        abort(404)
    
    user = User.query.filter_by(email=email).first()
    try: 
        session['user_info'].email_verified = True
        user.email_verified = True
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        Log.error(str(e))
        raise e
    
    activated = True
    
    return redirect(url_for('.main', user_activated=activated))
    
#########################################################################
def generate_verification_token(email):
    s = URLSafeTimedSerializer('secret_key')
    return s.dumps(email, salt='security-salt')

def confirm_token(token, expiration=3600):
    s = URLSafeTimedSerializer('secret_key')
    try:
        email = s.loads(
            token,
            salt='security-salt',
            max_age=expiration
        )
    except:
        return False
    
    return email
    
def create_token_link(token):
    base_url = 'http://port-2000.miniweb-ricopanda0821566506.codeanyapp.com'
    token_link = base_url + url_for('.activate_user', token=token, __external=True)
    return token_link
    