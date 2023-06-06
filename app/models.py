from app import db
from datetime import datetime

# User class is for admin role that only has access to website
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
class UserLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    rfidTagNum = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    checkInTime = db.Column(db.String(1000))
    checkInDate = db.Column(db.String(1000))

class TagUser(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    rfidTagNum = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    data = db.Column(db.String(1000))

class MotionLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uuid = db.Column(db.String(1000))
    message = db.Column(db.String(1000))
    checkInTime = db.Column(db.String(1000))
    checkInDate = db.Column(db.String())



