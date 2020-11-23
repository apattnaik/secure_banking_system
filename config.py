import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:////tmp/sbs.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = b'\x80$\x8ep\x0e\xf9\xee\r\xa2\xe1\xdd\x16\x18\xaf\xd3\x15'
    SESSION_TYPE = 'filesystem'
