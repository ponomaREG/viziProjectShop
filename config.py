import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    DATABASES_FOLDER = os.path.join(basedir,'databases')
    DB_SHOP = os.path.join(DATABASES_FOLDER,'shop.db')
    JSON_AS_ASCII = False