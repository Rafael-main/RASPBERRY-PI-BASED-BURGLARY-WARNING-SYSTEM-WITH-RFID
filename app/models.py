from rfidapp import sqlite
# import sqlite3
import rfidapp.secrets as secrets



class record(object):
    def __init__(self, userid = None, username=None, password=None):
        self.userid = userid
        self.username = username
        self.password = password
        self.password_process = secrets.Secreto()

    

    def signUp (self):
        cursor = sqlite.cursor()
        hashed_pass = self.password_process.to_hash(self.password)
        user = (self.userid, self.username, hashed_pass)
        sql = """INSERT INTO users (user_id, username, password) VALUES(
            ?,?,?
            )"""

        try:
            cursor.execute(sql, user)
            sqlite.commit()
            print(f'userid: {self.userid}\nusername: {self.username}\npassword: {hashed_pass}')
            return 'success'
        except Exception as e:
            print(e)
            return 'error'

    
    def login (self):
        # print(self.username)
        cursor = sqlite.cursor()
        sql = """SELECT  * FROM users WHERE username='%s'""" % (self.username)

        try:
            cursor.execute(sql)
            data = cursor.fetchone()
            print(data)
            password = self.password_process.to_process(self.password)
            if self.password_process.check_hash(password, data[2]):
                return data
            else:
                return 'wrong_pass'
        except Exception as e:
            print(e)
            return 'non_exist'


