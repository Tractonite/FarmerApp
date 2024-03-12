from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login')
def login():
    return render_template('admin/login.html')

@admin_bp.route('/signup')
def signup():
    return render_template('admin/signup.html')

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/products')
def products():
    return render_template('admin/products.html')

@admin_bp.route('/users')
def users():
    return render_template('admin/users.html')