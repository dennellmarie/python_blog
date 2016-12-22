import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from flask.ext.login import UserMixin
from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



# create the 'Entry' table with the following attributes
class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)



# create users of the blog. only authenticated users will be allowed to add posts
class User(Base, UserMixin):                      # Creating the User model from Base
    __tablename__ = "users"                       # SQL table name: 'users'

    id = Column(Integer, primary_key=True)        # primary key is user.id
    name = Column(String(128))                    # user's name
    email = Column(String(128), unique=True)      # user's email must be a unique field
    password = Column(String(128))                # user's password



# SQLAlchemy engine to create the tables
Base.metadata.create_all(engine)