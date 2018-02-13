import os.path


basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
#SQLALCHEMY_DATABASE_URI = 'postgresql++pg8000://postgres:password@localhost/webpanel'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

SECRET_KEY = 'myultrasecret0'

