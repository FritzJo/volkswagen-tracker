import os

#If you want to use any other way to handle credentials, just edit these functions


def get_username():
    return os.environ['VW_USERNAME']


def get_password():
    return os.environ['VW_PASSWORD']


def get_database_type():
    return os.environ['VW_DATABASE_TYPE']


def get_database_host():
    return os.environ['VW_DATABASE_HOST']


def get_database_port():
    return os.environ['VW_DATABASE_PORT']


def get_database_user():
    return os.environ['VW_DATABASE_USER']


def get_database_pass():
    return os.environ['VW_DATABASE_PASS']


def get_update_interval():
    return os.environ['VW_UPDATE_INTERVAL']
