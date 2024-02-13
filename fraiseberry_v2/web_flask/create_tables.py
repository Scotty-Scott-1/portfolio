#!/usr/bin/python3

from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy import MetaData, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sys import argv

user_name = argv[1]
password = argv[2]
db_name = argv[4]
host = argv[3]
db_url = "mysql+mysqldb://{}:{}@{}/{}".format(user_name, password, host, db_name)


engine = create_engine(db_url, echo=True, pool_pre_ping=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(50))
    date_of_birth = Column(Date)
    email = Column(String(100), unique=True)
    user_password = Column(String(255), nullable=False, server_default="")
    is_active = Column(Boolean, nullable=False, server_default="0")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow)
    next_update = Column(DateTime, default=datetime.utcnow)
    intentions = Column(String(200))
    user_preferences = Column(Integer)
    user_name = Column(String(50), nullable=False, unique=True )

class User_preferences(Base):
    __tablename__ = "User_preferences"
    preferences_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id), unique=True)
    min_age = Column(Integer)
    max_age = Column(Integer)
    distance = Column(Integer)
    gender = Column(String(200))
    intentions = Column(String(200))
class Likes(Base):
    __tablename__ = "Likes"
    like_id = Column(Integer, primary_key=True, autoincrement=True)
    user_1_id = Column(Integer, ForeignKey(Users.id))
    user_2_id = Column(Integer, ForeignKey(Users.id))
    is_matched = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
class Matches(Base):
    __tablename__ = "Matches"
    match_id = Column(Integer, primary_key=True, autoincrement=True)
    user_1_id = Column(Integer, ForeignKey(Users.id))
    user_2_id = Column(Integer, ForeignKey(Users.id))
    created_at = Column(DateTime, default=datetime.utcnow)
class Messages(Base):
    __tablename__ = "Messages"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey(Users.id))
    receiver_id = Column(Integer, ForeignKey(Users.id))
    content = Column(Text)
    sent_at = Column(DateTime, default=datetime.utcnow)
Base.metadata.create_all(engine)