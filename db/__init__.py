from mongoengine import connect
from flask import current_app

def initialize_db():
    connect(
        db=current_app.config['MONGODB_SETTINGS']['db'],
        host=current_app.config['MONGODB_SETTINGS']['host'],
        port=current_app.config['MONGODB_SETTINGS']['port']
    )
