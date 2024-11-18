# 기본설정

from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()

# URI 설정 맞추기 

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:0000@localhost/oz_form"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_ECHO = False
    reload = True
