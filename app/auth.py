from flask import Blueprint, redirect, url_for, render_template, flash, session
from app import db

from app.forms import LoginForm, SignUpForm
from app.modelsdels import User
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/welcome', methods=['GET', 'POST']) 
def welcome():
    signup_form = SignUpForm()
    login_form = LoginForm()
    if signup_form.validate_on_submit():
        userid = f'user-{str(uuid.uuid4())[:5]}'
        # signUpdb = models.record(userid = userid, username = signup_form.username.data, password=signup_form.password.data)
        # signUp_status = signUpdb.signUp()
        user = User(name = signup_form.username.data, password=signup_form.password.data)
        db.session.add()
        db.commit()
        
        if signUp_status == 'success':
            session.permanent = True
            # loginStatusAndData = signUpdb.login()  # loginStatusAndData mo return na sya sa data sa user na gi login if valid

            session['user'] = loginStatusAndData
            return redirect(url_for('home'))
           
        else:
            flash('Username Already Exist!', 'warning')
        # return redirect(url_for('home'))

    elif login_form.validate_on_submit():
        session.permanent = True
        # logindb = models.record(username = login_form.login_username.data, password=login_form.login_password.data)

        # loginStatusAndData= logindb.login() # loginStatusAndData mo return na sya sa data sa user na gi login if valid

        if loginStatusAndData == 'wrong_pass' or loginStatusAndData == 'non_exist':
            flash('Wrong Username or Password!', 'danger')
        else:
            session['user'] = loginStatusAndData
            return redirect(url_for('home'))
    
    return render_template('welcome.html', loginForm = login_form, signupForm = signup_form)


    return 'Sign up'

@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('welcome'))