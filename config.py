import os

# Set the database URI based on environment variables
DATABASE_URI = os.environ.get('DATABASE_URI')

# Define the app configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI or 'mysql://root:password@localhost:3306/farmer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"