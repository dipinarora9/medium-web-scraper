import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'sqlite:///abc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    RUN_AUTOCOMPLETER = os.environ.get('RUN_AUTOCOMPLETER', True)
