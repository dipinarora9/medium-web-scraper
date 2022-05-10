import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///abc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
