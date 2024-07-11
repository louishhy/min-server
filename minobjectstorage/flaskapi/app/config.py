import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', default='default')