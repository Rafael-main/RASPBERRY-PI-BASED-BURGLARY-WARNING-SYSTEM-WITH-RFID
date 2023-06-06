from flask import jsonify
from app.models import TagUser, User, UserLogs, MotionLogs
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
            

class UserLogsController:
    def __init__(self, uuid='', rfidTagNum='', name='', checkInTime=None, checkInDate=None):
        self.uuid = uuid
        self.rfidTagNum = rfidTagNum
        self.name = name
        self.checkInTime = checkInTime
        self.checkInDate = checkInDate
    
    def add_logs(self):
        try:
            log = UserLogs(uuid=self.uuid, rfidTagNum = self.rfidTagNum, name = self.name, checkInTime = self.checkInTime, checkInDate = self.checkInDate)
            db.session.add(log)
            db.session.commit()
            return {'status':'ok', 'message': 'log added'}
        except:
            return {'status': 'failed', 'message': 'request failed'}
    def logs(self):
        try:
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
            return {'status':'success', 'message':'request provided', 'data':tojsonifyAllLogs}
        except:
            return {'status':'failed', 'message':'request failed'}

class MotionLogsController:
    def __init__(self, message='', checkInTime=None, checkInDate=None):
        self.message = message
        self.checkInTime = checkInTime
        self.checkInDate = checkInDate
    
    def add_motion_log(self):
        try:
            motionLog = MotionLogs(message = self.message, checkInTime = self.checkInTime, checkInDate = self.checkInDate)
            db.session.add(motionLog)
            db.session.commit()
            return {'status':'ok', 'message':'motion detected!'}
        except:
            return {'status':'failed', 'message':'request failed'}
    
    def read_all_motion_logs(self):
        try:

            tojsonifyAllLogs = []
            allOfTheLogs = MotionLogs.query.all()
            print(allOfTheLogs)
            for log in allOfTheLogs:
                print(log.uuid)
                print(log.name)
                tojsonifyAllLogs.append({
                    'message' : log.name,
                    'checkInTime' : str(log.checkInTime),
                    'checkInDate' : str(log.checkInDate),
                })
            return {'status':'success', 'message':'request provided', 'data':tojsonifyAllLogs}
        except:

            return {'status':'failed', 'message':'request failed'}


class TagUserController:
    def __init__(self, uuid='', rfidTagNum='', name='', data=''):
        self.uuid=uuid
        self.rfidTagNum=rfidTagNum
        self.name=name
        self.data=data

    def add_tag_user(self):
        try:

            all_tag_user = TagUser().query.all()
            for one_tag_user in all_tag_user:
                if one_tag_user.rfidTagNum == self.rfidTagNum:
                    return {'status': 'failed', 'message':'user already in database'}
            tag_user = TagUser(uuid=self.uuid, rfidTagNum=self.rfidTagNum, name=self.name, data=self.data)
            db.session.add(tag_user)
            db.session.commit()
            return {'status':'ok', 'message':'successfully added user'}
        except:
            return {'status':'failed', 'message':'request failed'}
        
    def update_tag_user(self, id):
        try:
            updateTag = TagUser.query.filter_by(id=id).first()
            updateTag.rfidTagNum=self.rfidTagNum
            updateTag.name=self.name
            updateTag.data=self.data

            db.session.commit()
            return {'status':'ok', 'message':'successfully updated user'}
        except:
            return {'status':'failed', 'message':'request failed'}
        
    def del_tag_user(self, id):
        try:
           TagUser.query.filter_by(id=id).delete() 
           db.session.commit()
           return {'status':'ok', 'message':'successfully deleted user'}
        except:
            return {'status':'failed', 'message':'request failed'}
        
    def read_tag_user(self):
        try:
            all_tag_user = TagUser.query.all()
            tag_user_list = []

            for one_tag_user in all_tag_user:
                tag_user_list.append({
                    'id': one_tag_user.id,
                    'uuid': one_tag_user.uuid,
                    'rfidTagNum': one_tag_user.rfidTagNum,
                    'data': one_tag_user.data
                })

            return {'status':'success', 'message':'request provided', 'data':tag_user_list}
        except:
            return {'status':'failed', 'message':'request failed'}
        