import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shush'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLITE3_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                           os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    BASE_URL = "https://api.cardmarket.com/ws/v2.0/output.json/"
    AUTH_FILE = os.path.join(basedir, 'auth.txt')
