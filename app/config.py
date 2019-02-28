import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TWILIO_ACCOUNT_SID = 'AC45cfdd30d2d97c83313d5234b0a545fd'
    TWILIO_AUTH_TOKEN = '0a724904ae5059e6ab4d03fba376638e'
    TWILIO_NUMBER = '+14156902181'
    APPLICATION_SID = 'AP6759837a153826a3ae52be5d0d15e6b4'