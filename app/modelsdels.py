from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class AuthorizedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    rfidTagNum = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class UserLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    rfidTagNum = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    checkedIn = db.Column(db.DateTime())


