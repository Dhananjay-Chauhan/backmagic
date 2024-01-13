from flask_login import current_user
from api import db
from api import admin
from flask import redirect, url_for, request
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_admin.contrib.sqla import ModelView 


class Leaderboard(db.Model):
    reg_no = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(25), nullable=False)
    member_type = db.Column(db.String(10),nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, default=0)
    contributions = db.Column(db.Integer, default=0)
    contribution_details = db.Column(db.Text, default=" ", nullable=True)
    photo = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"{self.reg_no}-{self.name}"
    

class ModelViewLeaderboard(ModelView) :
    form_columns = ['reg_no', 'name','department','member_type','phone_no','email','points','contributions','contribution_details','photo'] 

        
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

admin.add_view(ModelViewLeaderboard(Leaderboard,db.session))