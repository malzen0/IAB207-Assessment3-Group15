from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# Logging in as a user
@auth_bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error,'danger')
    return render_template('user.html', form=login_form, heading='Login')

# Registering a user
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_name = register_form.user_name.data
        email_id = register_form.email_id.data
        mobile_num = register_form.mobile_num.data
        address = register_form.address.data
        password = register_form.password.data
        
        # Check if the username already exists 
        existing_user = User.query.filter_by(name=user_name).first()
        if existing_user is None:
            # Create a new user 
            new_user = User(name=user_name, 
                            email_id=email_id, 
                            mobile_num=mobile_num,
                            address=address, 
                            password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exists. Please choose a different username', 'warning')
    return render_template('user.html', form=register_form, heading='Register') 

# Logout user
@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))
            