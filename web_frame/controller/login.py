# -*- coding: utf-8 -*-

from flask import redirect, render_template, request, session, url_for
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from web_frame.web_blueprint import web_frame
from web_frame.web_logger import Log
from web_frame.model import db 
from web_frame.model.user import User
from web_frame.controller.general import login_required, get_user

  
@web_frame.route('/')
@login_required
def index():
    return redirect(url_for('.main'))

@web_frame.route('/user/login')
def login_form():
   
    if 'user_info' in session:
        return redirect(url_for('.main'))
        
    next_url = request.args.get('next','')
    regist_username = request.args.get('regist_username','')
    update_username = request.args.get('update_username','')
    recover_mail = request.args.get('recover_mail','')
    Log.info('(%s)next_url is %s' % (request.method, next_url))
    
    form = LoginForm(request.form)
    
    return render_template('login.html',
                           next_url=next_url,
                           form=form,
                           regist_username=regist_username,
                           update_username=update_username)

@web_frame.route('/user/login', methods=['POST'])
def login():

    form = LoginForm(request.form)
    next_url = form.next_url.data
    login_error = None
    
    if form.validate():
        session.permanent = True
        
        username = form.username.data
        password = form.password.data
        next_url = form.next_url.data
        
        Log.info('(%s)next_url is %s' % (request.method, next_url))
        
        user = get_user(username)
            
        if user:
            if not check_password_hash(user.password, password):
                login_error = 'Invalid password'
                
            else:
                session['user_info'] = user
                Log.info('%s has logged in' % user)
                if user.admin:
                    return redirect(url_for('admin.index'))
                elif next_url != '': 
                    return redirect(next_url)
                else:
                    return redirect(url_for('.main'))
        
        else: 
            login_error = 'User does not exist'
            
    return render_template('login.html',
                           next_url=next_url,
                           form=form,
                           error=login_error)
    
@web_frame.route('/logout')
@login_required
def logout():
    
    Log.info('%s has logged out' % session['user_info'])
    session.clear()
    
    return redirect(url_for('.index'))

############################################################################
class LoginForm(Form):
    
    username = TextField('Username',
                         [validators.Required('Enter user name'),
                          validators.Length(
                            min=4,
                            max=20,
                            message='4~20 characters')])
    
    password = PasswordField('New Password',
                             [validators.Required('Enter password'),
                              validators.Length(
                                min=4,
                                max=20,
                                message='4~20 characters')])
    
    next_url = HiddenField('Next URL')
   