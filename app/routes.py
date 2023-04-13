from app.controller import Logs, UserController
from app.modelsdels import User
from app import db
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from app import app

from app.forms import LoginForm, SignUpForm
import app.models as models
import uuid
from datetime import datetime


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
            if curr_user != 'wrong_pass' or curr_user != 'non-exist':
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
        if attemptCurrUser == 'wrong_pass' or attemptCurrUser == 'non-exist':
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

@app.route('/userlogs')
def userlogs():
    if 'user' in session:
        logsOfUsers = Logs()

        return jsonify(logsOfUsers.logs())

    flash('Wrong Username or Password! Try Again.', 'danger')
    return render_template('welcome.html')
