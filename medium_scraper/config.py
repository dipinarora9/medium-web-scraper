import os

from medium_scraper.helpers.constants import LOCAL_DATABASE_LOCATION


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', f"sqlite:///{LOCAL_DATABASE_LOCATION}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    RUN_AUTOCOMPLETER = os.environ.get('RUN_AUTOCOMPLETER', False)
    AUTO_COMPLETE_URL = os.environ.get(
        'AUTO_COMPLETE_URL',
        'https://medium-web-scraper-c5zky.ondigitalocean.app')
