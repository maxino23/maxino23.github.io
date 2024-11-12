from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for flash messages and sessions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Increased length for hashed passwords

# Define route for index.html
@app.route("/")
def index():
    return render_template('index.html')  # Ensure 'index.html' is in the templates folder

@app.route("/sign_in")
def sign_in():
    return render_template('sign_in.html')
@app.route("/add_user", methods=['POST'])
def add_user():
    email = request.form.get("email")
    password = request.form.get("pass")

    if not email or not password:
        flash("Email and password are required.", "error")
        return redirect(url_for('index'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered. Please use a different email.", "error")
        return redirect(url_for('index'))

    # Hash password with updated method
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    flash("Successfully registered!", "success")
    return redirect(url_for('index'))


# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the app with debugging enabled
