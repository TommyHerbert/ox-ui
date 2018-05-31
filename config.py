import os


class Config(object):
    FLASK_APP = 'ox.py'
    SECRET_KEY = os.environ.get('SECRET_KEY')
