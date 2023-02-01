from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class AuthorizedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    rfidTagNum = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class CheckedIn(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    rfidTagNum = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    checkedIn = db.Column(db.DateTime())


