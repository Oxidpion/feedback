import os
from datetime import datetime


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    REDMINE_URL = os.environ.get('REDMINE_URL')
    REDMINE_KEY = os.environ.get('REDMINE_KEY')

    LOAD_ASSIGNMENT_FROM = laf = datetime.strptime(
        os.environ.get('LOAD_ASSIGNMENT_FROM', '2019-01-01'), '%Y-%m-%d').date()

    DEFAULT_EXCLUDED_PROJECT_IDS = list(
        map(int, os.environ.get('DEFAULT_EXCLUDED_PROJECT_IDS', '').split(',')))
