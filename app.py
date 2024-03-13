from flask import Flask, render_template, session, request, Response, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db import db_init, db
from models.user import User
from models.product import Product
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Initialize the app and set the configuration
app = Flask(__name__, template_folder='template')
app.config.from_object(Config)

# Initialize the database
db_init(app)
Session(app)

# Register the Blueprints
from views.admin import admin_bp
from views.product import product_bp
from views.user import user_bp

app.register_blueprint(admin_bp)
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)

# Define a default route
@app.route('/')
def index():
    return render_template('index.html')

#static file path
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return render_template("error.html", message="Unauthorized access. Admin role required.")
        return f(*args, **kwargs)
    return decorated_function

def is_farmer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            if session.get("role") != "farmer":
                return render_template("error.html", message="Unauthorized access. Admin role required.")
        return f(*args, **kwargs)
    return decorated_function

# Authenticate User
# @app.route("/auth", methods=["POST"])
# def auth():
#     username = request.form["username"]
#     password = request.form["password"]

#     cursor = mysql.connection.cursor()
#     query = "SELECT * FROM users WHERE username=%s"
#     cursor.execute(query, (username,))
#     user = cursor.fetchone()

#     if user and bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
#         session["username"] = username
#         return redirect("/dashboard")
#     else:
#         return render_template("login.html", error="Invalid username or password")
    
#signup as admin
@app.route("/admin/signup", methods=["GET","POST"])
def signup():
	if request.method=="POST":
		session.clear()
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		if(password!=repassword):
			return render_template("error.html", message="Passwords do not match!")

		#hash password
		pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
		
		fullname = request.form.get("fullname")
		username = request.form.get("username")
		#store in database
		new_user =User(username=username,email=fullname,password=pw_hash,is_admin=True)
		try:
			db.session.add(new_user)
			db.session.commit()
		except:
			return render_template("error.html", message="Username already exists!")
		return render_template("admin/login.html", msg="Account created!")
	return render_template("admin/signup.html")

#login as admin
@app.route("/admin/login", methods=["GET", "POST"])
def login():
	if request.method=="POST":
		session.clear()
		username = request.form.get("username")
		password = request.form.get("password")
		result = User.query.filter_by(username=username).first()
		print(result)
		# Ensure username exists and password is correct
		if result == None or not check_password_hash(result.password, password):
			return render_template("error.html", message="Invalid username and/or password")
		# Remember which user has logged in
		session["username"] = result.username
		session["role"] = "admin"
		return redirect("/admin/dashboard")
	return render_template("admin/login.html")

#signup as farmer
@app.route("/farmer/signup", methods=["GET","POST"])
def signup_farmer():
	if request.method=="POST":
		session.clear()
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		if(password!=repassword):
			return render_template("error.html", message="Passwords do not match!")

		#hash password
		pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
		
		username = request.form.get("username")
		email = request.form.get("email")
		#store in database
		new_user =User(username=username,email=email,password=pw_hash,is_farmer=True)
		try:
			db.session.add(new_user)
			db.session.commit()
		except e:
			print(e)
			return render_template("error.html", message="Username already exists!")
		return render_template("farmer/login.html", msg="Account created!")
	return render_template("farmer/signup.html")

#login as farmer
@app.route("/farmer/login", methods=["GET", "POST"])
def login_farmer():
	if request.method=="POST":
		session.clear()
		username = request.form.get("username")
		password = request.form.get("password")
		result = User.query.filter_by(username=username).first()
		print(result)
		# Ensure username exists and password is correct
		if result == None or not check_password_hash(result.password, password):
			return render_template("error.html", message="Invalid username and/or password")
		# Remember which user has logged in
		session["username"] = result.username
		session["role"] = "farmer"
		return redirect("/farmer/dashboard")
	return render_template("farmer/login.html")

#signup as user
@app.route("/signup", methods=["GET","POST"])
def signup_user():
	if request.method=="POST":
		session.clear()
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		if(password!=repassword):
			return render_template("error.html", message="Passwords do not match!")

		#hash password
		pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
		
		username = request.form.get("username")
		email = request.form.get("email")
		#store in database
		new_user =User(username=username,email=email,password=pw_hash,is_farmer=True)
		try:
			db.session.add(new_user)
			db.session.commit()
		except e:
			print(e)
			return render_template("error.html", message="Username already exists!")
		return render_template("farmer/login.html", msg="Account created!")
	return render_template("farmer/signup.html")

#login as user
@app.route("/login", methods=["GET", "POST"])
def login_user():
	if request.method=="POST":
		session.clear()
		username = request.form.get("username")
		password = request.form.get("password")
		result = User.query.filter_by(username=username).first()
		print(result)
		# Ensure username exists and password is correct
		if result == None or not check_password_hash(result.password, password):
			return render_template("error.html", message="Invalid username and/or password")
		# Remember which user has logged in
		session["username"] = result.username
		session["role"] = "farmer"
		return redirect("/farmer/dashboard")
	return render_template("farmer/login.html")

#logout
@app.route("/logout")
def logout():
	session.clear()
	return redirect("admin/login")


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
	return render_template("admin/dashboard.html")

@app.route("/farmer/dashboard")
@is_farmer
def farmer_dashboard():
	return render_template("farmer/dashboard.html")


## Farmer controllers
# add prodcut
@app.route("/farmer/add", methods=["GET", "POST"])
def login_farmer():
	if request.method=="POST":
		name = request.form.get("name")
		desc = request.form.get("desc")
		price = request.form.get("price")
		unit = request.form.get("unit")
		new_user = 
		try:
			db.session.add(new_user)
			db.session.commit()
		except e:
			print(e)
			return render_template("error.html", message="Error adding")
		return redirect("/farmer/dashboard")
	return render_template("farmer/login.html")

	



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
