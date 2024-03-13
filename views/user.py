from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)

@user_bp.route('/login')
def login():
    return render_template('user/login.html')

@user_bp.route('/register')
def register():
    return render_template('user/signup.html')

@user_bp.route('/profile')
def profile():
    return render_template('user/profile.html')