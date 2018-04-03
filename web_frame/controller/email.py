# -*- coding: utf-8 -*-

from flask import abort, redirect, render_template, request, session, url_for
from flask_mail import Message

from web_frame.web_mail import mail
from web_frame.web_blueprint import web_frame
from web_frame.web_logger import Log
from web_frame.model import db
from web_frame.model.user import User
from web_frame.controller.general import get_user, login_required
from web_frame.controller.token import generate_verification_token, create_token_link

    
@web_frame.route('/user/send_recover_email')
def send_recover_email():
    
    email = request.args.get('email','')
    recover_account = User.query.filter_by(email=email).first()
    
    username = recover_account.username
    password = recover_account.password
    
    msg = Message()
    msg.html = render_template('email/recover.html', username=username, password=password)
    msg.recipients = [email]
    
    try:
        mail.send(msg)
        Log.info('Recovery mail sent to %s' % (username))
        recover_mail = 'E-mail successfully sent!'
        return redirect(url_for('.recover_account', recover_mail=recover_mail))
    except Exception as e:
        Log.error(str(e))
        raise e
    
    return redirect(url_for('.recover_account'))

@web_frame.route('/user/send_token_email')
@login_required
def send_token_email():
    
    current_user = get_user(session['user_info'].username)
    if current_user.email_verified:
        return redirect(url_for('.main'))
    
    username = current_user.username
    email = current_user.email
    
    token = generate_verification_token(email)
    confirm_url = create_token_link(token)
    msg = Message("Account verification")
    msg.html = render_template('email/activation.html', confirm_url=confirm_url)
    msg.recipients = [email]
    
    try:
        mail.send(msg)
        Log.info('Verification mail sent to %s' % (username))
        return redirect(url_for('.main', email_sent=True))
    except Exception as e:
        Log.error(str(e))
        raise e
    
    return redirect(url_for('.main', email_error=True))
    
