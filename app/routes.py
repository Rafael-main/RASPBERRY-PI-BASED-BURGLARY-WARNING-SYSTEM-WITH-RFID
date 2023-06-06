from app.controller import MotionLogsController, TagUserController, UserController, UserLogs, UserLogsController
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from app import app

from app.forms import LoginForm, SignUpForm
import uuid
from datetime import datetime

from app.models import TagUser

rfid_tags = {}
scanned_rfid = ''
curr_href = ''

@app.route('/')
def land():
    return redirect(url_for('welcome'))

@app.route('/welcome', methods=['GET','POST'])
def welcome():
    login_form = LoginForm()
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():

        # create a uuid for a user 
        userid = f'user-{str(uuid.uuid4())[:5]}'

        # initialize user that attempts to log in
        userController = UserController(uuid = userid, username = signup_form.username.data, password = signup_form.password.data)
 
        isUserRegistered = userController.addUser()
        # check if user is already signed up with app
        if (isUserRegistered == 'success'):
            session.permanent = True
            # login user
            curr_user = userController.loginUser()
            if curr_user != 'wrong_pass' or curr_user != 'non_exist':
                session['user'] = curr_user
                # return redirect(url_for('welcome'))
                return render_template('welcome.html', loginForm = login_form, signupForm = signup_form)
                  
        else: 
            flash('Username Already Exists!', 'warning')
        
        return redirect(url_for('home'))
        

    elif login_form.validate_on_submit():
        session.permanent = True
        logUserIn = UserController(username = login_form.login_username.data, password=login_form.login_password.data)
        attemptCurrUser = logUserIn.loginUser()
        print(attemptCurrUser)
        if attemptCurrUser == 'wrong_pass' or attemptCurrUser == 'non_exist':
            flash('Wrong Username or Password! Try Again.', 'danger')

        else:
            now = datetime.now()
            jsonifiedUser = {
                'uuid': str(attemptCurrUser.uuid),
                'username': attemptCurrUser.name,
                'timein': now.strftime("%H:%M:%S"),
                'datein': now.strftime("%d/%m/%Y"),
                'permitStats': 'Allow'
            }
            session['user'] = jsonifiedUser
            return render_template('home.html', userData = session['user'])

    
    return render_template('welcome.html', loginForm = login_form, signupForm = signup_form)


@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('welcome'))


@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', userData = session['user'])
    else:
        return redirect(url_for('welcome'))

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/create')
def create():
    if 'user' in session:
        print(request.url)
        return render_template('create.html')
    else:
        return redirect(url_for('welcome'))

@app.route('/tablemotion')
def tablemotion():
    if 'user' in session:
        return render_template('table_motion.html')
    else:
        return redirect(url_for('welcome'))

@app.route('/userlogs')
def userlogs():
    try:
        if 'user' in session:

            logsOfUsers = UserLogs()

            return jsonify(logsOfUsers.logs())

        flash('Wrong Username or Password! Try Again.', 'danger')
        return render_template('welcome.html')
    except:
        return jsonify({'message':'request pending...'})

@app.route('/add_logs', methods=['POST'])
def add_logs():
    try:
        if request.method == 'POST':
            res_post = request.get_json()
            log_uuid = f'log-{str(uuid.uuid4())[:5]}'
            rfid_tag_num = res_post['tag_id']
            rfid_tag_data = res_post['tag_data']
            tag = TagUser.query.filter_by(tag_id=rfid_tag_num).first()
            if tag:
                return jsonify({'status':'ok', 'message':'Already exists!'})

            user_log_controller = UserLogsController(uuid=log_uuid, rfidTagNum=rfid_tag_num, name=rfid_tag_data)
            user_log_controller_response = user_log_controller.add_logs()

        return jsonify(user_log_controller_response)
    except:
        return jsonify({'status': 'failed'})

@app.route('/motionlogs', methods=['GET'])
def motionlogs():
    try:
        motion_log_controller = MotionLogsController()
        motion_log_controller_response = motion_log_controller.read_all_motion_logs()

        return jsonify(motion_log_controller_response)
    except:
        return jsonify({'status': 'failed'})

@app.route('/motion', methods=['POST'])
def motion():
    try:
        if request.method == 'POST':
            res_post = request.get_json()
            message = res_post['message']
            motion_log_controller = MotionLogsController(message=message)
            motion_log_controller_response = motion_log_controller.add_motion_log()

        return jsonify(motion_log_controller_response)
    except:
        return jsonify({'status': 'failed'})

@app.route('/curr_route', methods=['GET','POST'])
def curr_route():
    data = ''
    if request.method == 'POST':
        res = request.get_json()
        data = res['data']
        curr_href = res['data']
        print(curr_href)
        print(data)

    return jsonify({'status': 'ok', 'data':data})

@app.route('/rfidtag')
def rfidtag():
    status_data = request.form.get('status')
    tag_id = request.form.get('tag_id')
    tag_data = request.form.get('tag_data')
    data = {
        'status': status_data,
        'tag_id': tag_id,
        'tag_data': tag_data
    }
    return jsonify({'status': 'ok', 'data': data})

@app.route('/read_tag', methods=['GET', 'POST'])
def read_tag():
    try:
        if request.method == 'POST':
            tag_id = request.form['tag_id']
            # Check if the tag exists in the database
            tag = TagUser.query.filter_by(tag_id=tag_id).first()
            if tag:
                if request.headers.get('User-agent'):
                    return jsonify({'status':'ok', 'message':'RFID tag exists in the database'})

            scanned_rfid = tag_id
            return jsonify({'status': 'ok', 'message':'RFID tag scanned', 'data': scanned_rfid})
        elif request.method == 'GET':
            return jsonify({'status': 'ok', 'data': scanned_rfid})
            
    except:
        return jsonify({'status':'failed', 'message':'Something went wrong...'})



# Route to check if RFID tag exists in the database
@app.route('/check_tag', methods=['POST'])
def check_tag():
    try:
        tag_id = request.form['tag_id']

        # Check if the tag exists in the database
        tag = TagUser.query.filter_by(tag_id=tag_id).first()
        if tag:
            return jsonify({'status':'ok', 'message':f'RFID tag exists in the database with data: {tag.tag_data}'})

        return jsonify({'status': 'does not exist', 'message':'RFID tag does not exist in the database'})
    except:
        return jsonify({'status':'failed', 'message':'Something went wrong...'})


@app.route('/rfid', methods=['POST'])
def create_rfid_tag():
    tag_uuid = f'tag-{str(uuid.uuid4())[:5]}'
    tag_id = request.form.get('userlogtag')
    tag_data = request.form.get('userlogname')
    name = request.form.get('userlogname')


    tag_user_controller = TagUserController(uuid=tag_uuid, rfidTagNum=tag_id, name=name, data=tag_data)

    tag_controller_response = tag_user_controller.add_tag_user()

    return jsonify(tag_controller_response)

# Read an existing RFID tag
@app.route('/rfid/', methods=['GET'])
def read_rfid_tag():
    tag_user_controller = TagUserController()

    tag_controller_response = tag_user_controller.read_tag_user()

    return jsonify(tag_controller_response)

# Update an existing RFID tag
@app.route('/rfid/<tag_id>', methods=['PUT'])
def update_rfid_tag(tag_id):
    update_record_json = request.get_json()
    rfid_tag_num = update_record_json['rfidtagnum']
    rfid_tag_name = update_record_json['tagname']
    rfid_tag_data = update_record_json['tagdata']
    tag_user_controller = TagUserController(rfidTagNum=rfid_tag_num, name=rfid_tag_name, data=rfid_tag_data)
    update_tag_user = tag_user_controller.update_tag_user(tag_id)
    return jsonify(update_tag_user)

# Delete an existing RFID tag
@app.route('/rfid/<tag_id>', methods=['DELETE'])
def delete_rfid_tag(tag_id):
    tag_user_controller = TagUserController()
    tag_response_controller = tag_user_controller.del_tag_user(tag_id)
    return jsonify(tag_response_controller)
