import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True  # Turns on debugging features in Flask
SECRET_KEY = 'Sm9obiBTY2hyb20g#2l_ja3MgYXNzZ'

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite://db.sqlite'
else:
    SQLALCHEMY_DATABASE_URI = ''

SQLALCHEMY_TRACK_MODIFICATIONS = False