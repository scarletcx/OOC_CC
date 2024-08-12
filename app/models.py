from mongoengine import Document, StringField, IntField, connect
from flask import Flask

app = Flask(__name__)
app.config.from_object('app.config')

# 连接到 MongoDB
connect(
    db=app.config['MONGODB_SETTINGS']['db'],
    host=app.config['MONGODB_SETTINGS']['host'],
    port=app.config['MONGODB_SETTINGS']['port']
)

class User(Document):
    UserID = StringField(required=True, unique=True)
    level = IntField(required=True)
    exp = IntField(required=True)
    RodName = StringField(required=True)
    BaitNumber = IntField(required=True)
    GMCNumber = IntField(required=True)
    Fishername = StringField(required=True)
    baitNumber = IntField(required=True)

    def __repr__(self):
        return f"<User(UserID='{self.UserID}', level={self.level}, exp={self.exp}, RodName='{self.RodName}', BaitNumber={self.BaitNumber}, GMCNumber={self.GMCNumber}, Fishername='{self.Fishername}', baitNumber={self.baitNumber})>"
