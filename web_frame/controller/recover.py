# -*- coding: utf-8 -*-

from flask import redirect, render_template, request, session, url_for
from werkzeug import generate_password_hash
from wtforms import Form, TextField, validators

from web_frame.web_blueprint import web_frame
from web_frame.web_logger import Log
from web_frame.model import db
from web_frame.model.user import User
from web_frame.controller.general import password_generator


@web_frame.route('/user/recover_account')
def recover_account_form():
    
    form = RecoverForm(request.form)
    recover_error = request.args.get('error','')
    recover_mail = request.args.get('recover_mail','')
    
    return render_template('recover.html', 
                            form=form, 
                            error=recover_error,
                            recover_mail=recover_mail)
    
@web_frame.route('/user/recover_account', methods=['POST'])
def recover_account():
    
    form = RecoverForm(request.form)
    recover_error = None
    if form.validate():
        
        email = form.email.data
        new_password = password_generator()
        
        try:
            current_user = User.query.filter_by(email=email).first()
        except Exception as e:
            Log.error(str(e))
        
        if not current_user:
            recover_error = 'No matching account!'
            return redirect(url_for('.recover_account', error=recover_error))
        
        if not current_user.email_verified:
            recover_error = 'Account not verified yet!'
            return redirect(url_for('.recover_account', error=recover_error))
   
        try:
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            return redirect(url_for('.send_recover_email', email=email))
            
        except Exception as e:
            db.session.rollback()
            Log.error(str(e))
            recover_error = 'Error!'
            raise e
            
    return render_template('recover.html', form=form, error=recover_error)
    
######################################################################
class RecoverForm(Form):
    
    email = TextField('Email',[validators.Required('Enter email.'),
                               validators.Email(message='Not a valid e-mail!')])
    

    
