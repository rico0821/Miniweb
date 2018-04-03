# -*- coding: utf-8 -*-

from web_frame.model import Base, db


class User(Base):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(100), unique=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    ################################################
    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)