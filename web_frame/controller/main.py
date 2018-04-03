# -*- coding: utf-8 -*-

from flask import current_app, redirect, render_template, request, session, url_for

from web_frame.web_blueprint import web_frame
from web_frame.web_logger import Log
from web_frame.model import db
from web_frame.model.user import User
from web_frame.controller.general import login_required, get_user


@web_frame.route('/main')
@login_required
def main():
    
    current_user = get_user(session['user_info'].username)
    username = current_user.username
    email_verified = current_user.email_verified
    email_sent = request.args.get('email_sent', '')
    email_error = request.args.get('email_error', '')
    user_activated = request.args.get('user_activated', '')
    
    if current_user.admin:
        return redirect(url_for('admin.index'))
    return render_template('main.html',
                           email_verified=email_verified,
                           email_sent=email_sent,
                           email_error=email_error,
                           user_activated=user_activated)