# from sqlalchemy import func
from api import app
import bcrypt
import os
from flask import render_template, flash, request, redirect, url_for,Response,send_file,jsonify
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from .models import *
from flask_cors import cross_origin
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

@app.route("/")
def index():
    return render_template('base.html',title='dhananjau')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/login",methods=['GET','POST'])
def login():
    print(bcrypt.hashpw("dhananjay".encode(),bcrypt.gensalt()).decode())
    if request.method=="POST":
        reg_no = request.form['reg_no']
        password = request.form['password']
        hash_password = Admins.query.filter_by(reg_no=reg_no).first()
        print("check :\n")
        # print(bcrypt.checkpw(password.encode(),hash_password.password.encode()))
        if bcrypt.checkpw(password.encode(),hash_password.password.encode()):
            login_user(hash_password)
            return redirect(url_for('success'))
        
    return render_template('login.html')


@app.route("/leaderboard")
def leaderboard():
    data = Leaderboard.query.all();
    members_data = []
    for member in data:
        temp = {}
        temp["name"] = member.name
        temp["reg_no"] = member.reg_no
        temp["department"] = member.department
        temp["member_type"] = member.member_type
        temp["phone_no"] = member.phone_no
        temp["email"] = member.email
        temp["points"] = member.points
        temp["contributions"] = member.contributions
        temp["contribution_details"] = member.contribution_details
        temp["photo"] = member.photo
        members_data.append(temp)
    return jsonify(members_data);

@app.route("/leaderboard/image/<reg_no>")
def member_image(reg_no):
    image = os.path.join("static","images","members",reg_no) + ".jpg"
    if not os.path.exists(image):
        Response(status=404)
    return send_file(image,mimetype="image/jpg")

@app.route("/gallery/image/<img_no>")
def gallery_image(img_no):
    image = os.path.join("static","images","gallery",img_no) + ".jpg"
    if not os.path.exists(image):
        Response(status=404)
    return send_file(image,mimetype="image/jpg")

@app.route("/event/videos/<name>")
def event_video(name):
    image = os.path.join("static","videos",name) + ".mp4"
    if not os.path.exists(image):
        Response(status=404)
    return send_file(image,mimetype="video/mp4")