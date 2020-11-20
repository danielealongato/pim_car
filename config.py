from os import environ, path
# from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SESSION_TYPE = environ.get('SESSION_TYPE')

    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:''@127.0.0.1/dani'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True