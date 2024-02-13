#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template, request, redirect, session as logged_in_session
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy import MetaData, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from create_tables import Users
from sys import argv



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
            session.close()
            logged_in_session["user_id"] = user.id
            return {"Success": "logged in: {}. User id: {}".format(user.user_name, user.id)}
        else:
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
            session.commit()
            return {"Success": "created new user"}

@app.route('/dashboard/', strict_slashes=False)
def dashboard():
    session = Session()
    user = session.query(Users).filter_by(id=logged_in_session.get("user_id")).first()
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
