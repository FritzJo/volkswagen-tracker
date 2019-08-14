import os


def get_username():
    return os.environ['CARNET_USERNAME']


def get_password():
    return os.environ['CARNET_PASSWORD']


def get_database_type():
    return os.environ['CARNET_DATABASE_TYPE']


def get_database_host():
    return os.environ['CARNET_DATABASE_HOST']


def get_database_port():
    return os.environ['CARNET_DATABASE_PORT']


def get_database_user():
    return os.environ['CARNET_DATABASE_USER']


def get_database_pass():
    return os.environ['CARNET_DATABASE_PASS']
