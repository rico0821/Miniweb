# -*- coding: utf-8 -*-

from flask import current_app, redirect, request, session, url_for, make_response, render_template
from werkzeug import generate_password_hash
from wtforms import TextField

from web_frame.model import db
from web_frame.web_logger import Log 
from web_frame.model.user import User
from web_frame.controller.login import login_required

from flask_admin import expose, Admin, AdminIndexView, BaseView, babel 
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as h


def render(self, template, **kwargs):
    kwargs['admin_view'] = self
    kwargs['admin_base_template'] = self.admin.base_template

    kwargs['_gettext'] = babel.gettext
    kwargs['_ngettext'] = babel.ngettext
    kwargs['h'] = h

    kwargs['get_url'] = self.get_url
    kwargs['config'] = current_app.config
    kwargs.update(self._template_args)

    response = make_response(render_template(template, **kwargs), 200)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

BaseView.render = render

class AdminAuth:
    
    def authorised(self):
        
        access = False
        username = session['user_info'].username
        current_user = User.query.filter_by(username=username).first()
        if current_user.admin:
            access = True
        return access
    
            
class AdminLogin(AdminIndexView, AdminAuth):
    @expose('/')
    @login_required
    def index(self):
        
        if self.authorised():
            print(self.is_accessible())
            return super(AdminLogin, self).index()
        else:
            return redirect(url_for('web_frame.main'))


        
class AuthModelView(ModelView, AdminAuth):
    @expose('/')
    @login_required
    def index_view(self):
        
        if self.authorised():
            return super(AuthModelView, self).index_view()
        else:
            return redirect(url_for('web_frame.main'))
    def on_model_change(self, form, User, is_created=False):
        if hasattr(form, "password"):
            User.password = generate_password_hash(form.password.data)
            

            
       
    
