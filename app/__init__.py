from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('app.config.Config')

mongo = PyMongo(app)

from app import routes  # 确保在最后导入 routes 以避免循环导入
