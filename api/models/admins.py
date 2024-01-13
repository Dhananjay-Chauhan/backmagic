from api import db
from api import admin
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from flask_login import UserMixin, login_manager, current_user
from flask import g, redirect, request, url_for


class Admins(db.Model, UserMixin):
    admin_id = db.Column(db.Integer,primary_key=True)
    reg_no = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.reg_no}-{self.admin_id}"
    
    def get_id(self):
        return self.admin_id


# class AdminHome(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated


class ModelViewAdmins(ModelView) :
    form_columns = ['admin_id','reg_no','password'] 
        
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))
   
# admin.add_view(AdminHome(name='', endpoint=''))
admin.add_view(ModelViewAdmins(Admins,db.session))