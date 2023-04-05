from app.modelsdels import User
from app import db
import app.secrets as secrets

class UserController:
    def __init__(self, uuid, username, password) :
        self.userUuid = uuid
        self.userUserName = username
        self.userPassword = password
        self.userPasswordProcess = secrets.Secreto()


    
    def addUser(self):
        try:
            hashed_pass = self.userPasswordProcess.to_hash(self.userPassword)
            user = User(uuid = self.userUuid, name = self.userUserName, password = hashed_pass)
            db.session.add(user)
            db.session.commit()

            return "success"
        except:
            return "failure"
        
    def loginUser(self):
        try:
            

