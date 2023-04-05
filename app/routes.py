from app.modelsdels import User
from app import db
from flask import render_template, redirect, request, session, url_for, flash, jsonify
from app import app

from app.forms import LoginForm, SignUpForm
import app.models as models
import uuid


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
        # signUpdb = models.record(userid = userid, username = signup_form.username.data, password=signup_form.password.data)
        # signUp_status = signUpdb.signUp()

        user = User(id = userid, name = signup_form.username.data, password = signup_form.password.data)
        db.session.add(user)
        db.session.commit()
 
        # get the first user in the database with a specific name
        curr_user = User.query.filter_by(name=signup_form.username.data).first()


        # check if user is already signed up with app
        if (curr_user != signup_form.username.data):
            session.permanent = True

            # login user
             
                
        else: 
            flash('Username Already Exists!', 'warning')
        
        return redirect(url_for('home'))
        
        # if signUp_status == 'success':
        #     loginStatusAndData = signUpdb.login()  # loginStatusAndData mo return na sya sa data sa user na gi login if valid

        #     session['user'] = loginStatusAndData
        #     return redirect(url_for('home'))
           
        # else:
        #     flash('Username Already Exist!', 'warning')
        # return redirect(url_for('home'))

    elif login_form.validate_on_submit():
        session.permanent = True
        # logindb = models.record(username = login_form.login_username.data, password=login_form.login_password.data)

        # loginStatusAndData= logindb.login() # loginStatusAndData mo return na sya sa data sa user na gi login if valid

        # if loginStatusAndData == 'wrong_pass' or loginStatusAndData == 'non_exist':
        #     flash('Wrong Username or Password!', 'danger')
        # else:
        #     session['user'] = loginStatusAndData
        #     return redirect(url_for('home'))
    
    return render_template('welcome.html', loginForm = login_form, signupForm = signup_form)


@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('welcome'))


@app.route('/home')
def home():
    # if 'user' in session:
    #     return render_template('home.html')
    # else:
    #     # return redirect(url_for('welcome'))
    return render_template('home.html')

@app.route('/table')
def table():
    return render_template('table.html')
