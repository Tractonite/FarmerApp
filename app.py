from flask import Flask, render_template, session, request, Response, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db import db_init, db
from models.user import User
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

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

# Authenticate User
@app.route("/auth", methods=["POST"])
def auth():
    username = request.form["username"]
    password = request.form["password"]

    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
        session["username"] = username
        return redirect("/dashboard")
    else:
        return render_template("login.html", error="Invalid username or password")
    
#signup as merchant
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
		new_user =User(username=username,email=fullname,password=pw_hash)
		try:
			db.session.add(new_user)
			db.session.commit()
		except:
			return render_template("error.html", message="Username already exists!")
		return render_template("admin/login.html", msg="Account created!")
	return render_template("admin/signup.html")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
