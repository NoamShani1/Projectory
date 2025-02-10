from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)  # Add the password column
    skills = db.Column(db.PickleType, default=list)  # Store as a list
    links = db.Column(db.PickleType, default=list)  # Store as a list
    cv_path = db.Column(db.String(200), nullable=True)  # Path to uploaded CV
