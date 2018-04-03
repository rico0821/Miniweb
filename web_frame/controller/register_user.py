# -*- coding: utf-8 -*-

import datetime

from flask import abort, redirect, render_template, request, session, url_for, jsonify
from werkzeug import generate_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from web_frame.web_blueprint import web_frame
from web_frame.web_logger import Log
from web_frame.model import db
from web_frame.model.user import User
from web_frame.controller.general import get_user, login_required
    
@web_frame.route('/user/regist')
def register_user_form():
  
    form = RegisterForm(request.form)
  
    return render_template('regist.html', form=form)

@web_frame.route('/user/regist', methods=['POST'])
def register_user():
  
    if 'user_info' in session:
        return redirect(url_for('.main'))
    
    form = RegisterForm(request.form)
  
    if form.validate():
    
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        try: 
            user = User(username=username,
                        email=email, 
                        password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            
            Log.debug(user)
            
        except Exception as e:
            error = "DB error occurs : " + str(e)
            Log.error(error)
            db.session.rollback()
            raise e
            
        else:
            return redirect(url_for('.login', regist_username=username))
    else:
        return render_template('regist.html', form=form)
    
@web_frame.route('/user/update_info/<username>')
@login_required
def update_user_form(username):

    if username != session['user_info'].username:
        abort(404)
    
    current_user = get_user(username)
    form = UpdateForm(request.form, current_user)
    
    return render_template('regist.html', user=current_user, form=form)

@web_frame.route('/user/update_info/<username>', methods=['POST'])
@login_required
def update_user(username):
    
    if username != session['user_info'].username:
        abort(404)
    
    current_user = get_user(username)
    form = UpdateForm(request.form)
    
    if form.validate():
        email = form.email.data
        password = form.password.data
        
        try: 
            current_user.email = email
            current_user.password = generate_password_hash(password)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            Log.error(str(e))
            raise e
            
        else:
            session['user_info'].email = current_user.email
            session['user_info'].password = current_user.password
            session['user_info'].password_confirm = current_user.password_confirm
            
            return redirect(url_for('.login', update_username=username))
    else:
        return render_template('regist.html', user=current_user, form=form)

@web_frame.route('/user/unregist')
@login_required
def unregist():
    user_id = session['user_info'].id
    
    try:
        user = User.query.filter_by(id=user_id).first()
        Log.info("unregist:"+user.username)
        
        if user.id == user_id:
            db.session.delete(user)
            db.session.commit()
            
        else:
            Log.error("Following user does not exist: %d", user_id)
            raise Exception
    
    except Exception as e:
        Log.error(str(e))
        db.session.rollback()
        raise error
        
    return redirect(url_for('.logout'))

@web_frame.route('/user/check_name', methods=['POST'])
def check_name():
    
    username = request.json['username']
    
    if get_user(username):
        return jsonify(result=False)
    else:
        return jsonify(result=True)
    
############################################################################    
class UpdateForm(Form):
    
    username = TextField('Username')
    email = TextField('Email',[validators.Required('Enter email.'),
                               validators.Email(message='Not a valid e-mail!')])
    password = PasswordField('New Password',
                              [validators.Required('Enter password.'),
                               validators.Length(
                                min=4,
                                max=50,
                                message='Must be between 4 and 50 characters.'),
                               validators.EqualTo('password_confirm',
                                                  message='Password mismatch!')])
    password_confirm = PasswordField('Confirm Password')
    
    username_check = HiddenField('Username Check', 
                                 [validators.Required('Check name availability.')])
        
############################################################################
class RegisterForm(Form):
    
    username = TextField('Username',
                          [validators.Required('Enter username.'),
                           validators.Length(
                            min=4,
                            max=50,
                            message='Must be between 4 and 50 characters.')])
    email = TextField('Email',[validators.Required('Enter email.'),
                               validators.Email(message='Not a valid e-mail!')])
    
    password = PasswordField('New Password',
                              [validators.Required('Enter password.'),
                               validators.Length(
                                min=4,
                                max=50,
                                message='Must be between 4 and 50 characters.'),
                               validators.EqualTo('password_confirm',
                                                  message='Password mismatch!')])
    password_confirm = PasswordField('Confirm Password')
    
    username_check = HiddenField('Username Check', 
                                 [validators.Required('Check name availability.')])
        