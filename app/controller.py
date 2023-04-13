from flask import jsonify
from app.modelsdels import User, AuthorizedUsers, UserLogs
from app import db
import app.secrets as secrets

class UserController:
    def __init__(self, uuid=None, username=None, password=None) :
        self.userUuid = uuid
        self.userUserName = username
        self.userPassword = password
        self.userPasswordProcess = secrets.Secreto()
    
    def addUser(self):
        try:
            hashed_pass = self.userPasswordProcess.to_hash(self.userPassword)
            user = User(uuid = self.userUuid, name = self.userUserName, password = hashed_pass)
            # find if curr_user (the user trying to sign in) is already signed up
            curr_user = User.query.filter_by(name=self.userUserName).all()
            if len(curr_user) <= 0:
                db.session.add(user)
                db.session.commit()
                return "success"

            return "failure"
        except Exception as e:
            return "Error: request unavailable"
        
    def loginUser(self):
        try:
            print(User.query.all())
            curr_user = User.query.filter_by(name=self.userUserName).first()
            password = self.userPasswordProcess.to_process(self.userPassword)
            if self.userPasswordProcess.check_hash(password, curr_user.password):
                return curr_user
            return 'wrong_pass'
        except:
            return 'non_exist'
            

class Logs:
    def logs(self):
        tojsonifyAllLogs = []
        allOfTheLogs = UserLogs.query.all()
        print(allOfTheLogs)
        for log in allOfTheLogs:
            print(log.uuid)
            print(log.name)
            tojsonifyAllLogs.append({
                'uuid' : log.uuid,
                'name' : log.name,
                'checkInTime' : str(log.checkInTime),
                'checkInDate' : str(log.checkInDate),
            })
        return tojsonifyAllLogs



class PowerUsers:
    def powerUsers(self):
        allAuthrzdUsers = AuthorizedUsers.query.all()
        print(allAuthrzdUsers)
        return allAuthrzdUsers