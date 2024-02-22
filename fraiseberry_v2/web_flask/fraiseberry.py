#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template, request, redirect, session as logged_in_session, send_file
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy import MetaData, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from create_tables import Users
from create_tables import User_preferences, User_pics
from sys import argv
import base64
import random

import os
import cv2




app = Flask(__name__, static_url_path='/static')
app.secret_key = "FRAISE"

user_name = argv[1]
password = argv[2]
db_name = argv[4]
host = argv[3]
db_url = "mysql+mysqldb://{}:{}@{}/{}".format(user_name, password, host, db_name)

engine = create_engine(db_url, echo=True, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

@app.route('/', strict_slashes=False)
def home():
    logged_in_session.clear()
    return render_template('homepage.html')

@app.route('/signin', strict_slashes=False, methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        form_data = request.json
        session = Session()

        user = session.query(Users).filter_by(user_name=form_data["user_name"]).first()

        if user and check_password_hash(user.user_password, form_data["user_password"]):
            logged_in_session["user_id"] = user.id
            user.latitude = form_data["latitude"]
            user.longitude = form_data["longitude"]

            today = datetime.today()
            age = datetime.strptime(str(user.date_of_birth), "%Y-%m-%d")
            real_age = today.year - age.year - ((today.month, today.day) < (age.month, age.day))
            user.age = real_age

            session.commit()

            result_user_name = user.user_name
            result_user_id = user.id
            session.close()


            return {"Success": "logged in: {}. User id: {}".format(result_user_name, result_user_id)}
        else:
            session.close()
            return {"Failed": "Username or password incorrect"}




@app.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('create-account.html')
    elif request.method == 'POST':
        form_data = request.json
        session = Session()

        existing_user = session.query(Users).filter_by(user_name=form_data["user_name"]).first()
        if existing_user:
            session.close()
            return {"Failed": "User name already exists"}


        hashed_password = generate_password_hash(form_data["user_password"])
        form_data["user_password"] = hashed_password

        new_user = Users(**form_data)
        with Session() as session:
            session.add(new_user)

            today = datetime.today()
            age = datetime.strptime(str(new_user.date_of_birth), "%Y-%m-%d")
            real_age = today.year - age.year - ((today.month, today.day) < (age.month, age.day))
            new_user.age = real_age

            session.commit()
            return {"Success": "created new user"}

@app.route('/dashboard/', strict_slashes=False)
def dashboard():
    session = Session()
    user = session.query(Users).filter_by(id=logged_in_session.get("user_id")).first()
    profile_pic = session.query(User_pics).filter_by(user_id=logged_in_session.get("user_id")).order_by(User_pics.id.desc()).first()
    session.close()
    if profile_pic:
        return render_template('dashboard2.html', user=user, profile_pic=profile_pic.path)
    return render_template('dashboard.html', user=user)

@app.route('/preferences/', strict_slashes=False, methods=['GET', 'POST'])
def preferences():
    session = Session()
    preferences = session.query(User_preferences).filter_by(user_id=logged_in_session.get("user_id")).first()
    if request.method == "GET":
        return render_template('update-preferences.html', preferences=preferences)
    elif request.method == 'POST':
        if preferences:
            form_data = request.json
            preferences.min_age = form_data["min_age"]
            preferences.max_age = form_data["max_age"]
            preferences.distance = form_data["distance"]
            preferences.gender = form_data["gender"]
            preferences.intentions = form_data["intentions"]
            session.commit()
            session.close()
            return {"success": "updated exiting preferences"}
        else:
            form_data = request.json
            new_preferences = User_preferences()
            new_preferences.min_age = form_data["min_age"]
            new_preferences.max_age = form_data["max_age"]
            new_preferences.distance = form_data["distance"]
            new_preferences.gender = form_data["gender"]
            new_preferences.intentions = form_data["intentions"]
            new_preferences.user_id = logged_in_session.get("user_id")

            session.add(new_preferences)
            session.commit()
            session.close()

            return {"Success": "created new preferences"}

@app.route('/camera/', strict_slashes=False, methods=['GET', 'POST'])
def camera():
        if request.method == "GET":
            return render_template('get_pic.html')
        if request.method == "POST":
            data = request.json

            _, encoded = data["ImageData"].split(",", 1)
            image_bytes = base64.b64decode(encoded)

            session = Session()
            user = session.query(Users).filter_by(id=logged_in_session.get("user_id")).first()

            filename = "{}{}.png".format(user.user_name, random.random());

            with open("static/images/user_pics/" + filename, "wb") as file:
                file.write(image_bytes)

            new_user_pics = User_pics()
            new_user_pics.user_id = user.id
            new_user_pics.file_name = filename
            new_user_pics.path = "static/images/user_pics/{}".format(filename)
            print(new_user_pics.path)

            session.add(new_user_pics)
            session.commit()

            session.close()

            return {"success": "saved file"}

@app.route('/swipe/', strict_slashes=False, methods=['GET', 'POST'])
def swipe():

    session = Session()
    prefs = session.query(User_preferences).filter_by(user_id=logged_in_session.get("user_id")).first()
    pref_gender = prefs.gender
    pref_min_age = prefs.min_age
    pref_max_age = prefs.max_age
    pref_distance = prefs.distance
    pref_intention = prefs.intentions
    session.close()

    session = Session()
    user = session.query(Users).filter_by(id=logged_in_session.get("user_id")).first()
    this_user_age = user.age
    this_user_user_name = user.user_name
    session.close()

    print("\n\n\n\n")
    print("The preferred gender is {}. Aged between {} and {}. Living {}km from the user. The user is interested in {}. The user is {} years old. Their username is {}."
          .format(pref_gender, pref_min_age, pref_max_age, pref_distance, pref_intention, this_user_age, this_user_user_name))
    print("\n\n\n\n")

    session = Session()
    candiate_list = session.query(Users).filter_by(gender=pref_gender).all()
    result = candiate_list
    session.close()



    return render_template('swipe.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
