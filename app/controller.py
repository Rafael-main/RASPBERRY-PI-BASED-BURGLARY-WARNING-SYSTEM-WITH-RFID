from flask import jsonify
from app.models import User, UserLogs
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
            

class UserLogsController:
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

# class FirmwareController:
#     def open_lock():
#         # Configure the GPIO pin for the solenoid lock
#         lock_pin = 18
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(lock_pin, GPIO.OUT)

#         # Activate the solenoid lock
#         GPIO.output(lock_pin, GPIO.HIGH)
#         time.sleep(5)  # Adjust the delay as needed

#         # Deactivate the solenoid lock
#         GPIO.output(lock_pin, GPIO.LOW)
#         GPIO.cleanup()
    
# # Function to control the buzzer
# def buzz_buzzer(num_times, interval):
#     # Configure the GPIO pin for the buzzer
#     buzzer_pin = 23
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(buzzer_pin, GPIO.OUT)

#     # Buzz the buzzer the specified number of times with the given interval
#     for _ in range(num_times):
#         GPIO.output(buzzer_pin, GPIO.HIGH)
#         time.sleep(interval)
#         GPIO.output(buzzer_pin, GPIO.LOW)
#         time.sleep(interval)

#     GPIO.cleanup()

# # Function to read RFID data and send it to the Flask server
# def read_rfid():
#     while True:
#         try:
#             # Read the RFID tag
#             tag_id, tag_data = reader.read()

#             # Validate the RFID tag and control the solenoid lock
#             if tag_id in rfid_tags:
#                 # Open the solenoid lock
#                 open_lock()
#                 # Activate the buzzer twice with an interval of 2 seconds
#                 buzz_buzzer(2, 2)
#             else:
#                 # Activate the buzzer three times with a one-second interval
#                 buzz_buzzer(3, 1)

#             # Send RFID data to the Flask server
#             payload = {'tag_id': tag_id, 'tag_data': tag_data}
#             requests.post('http://localhost:5000/rfid', data=payload)

#         except KeyboardInterrupt:
#             GPIO.cleanup()
#             break
    
#     # Function to validate the RFID tag
#     def validate_rfid(rfid_data):
#         # Implement your own validation logic here
#         # You can check against a database of valid RFID tags or use any other method
#         # For demonstration purposes, we assume a static valid RFID tag value
#         valid_rfid = '1234567890'
#         return rfid_data == valid_rfid
