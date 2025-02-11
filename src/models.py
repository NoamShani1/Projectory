from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)  # Correct definition of first_name
    last_name = db.Column(db.String(80), nullable=False)
    skills = db.Column(db.PickleType, default=list)
    links = db.Column(db.PickleType, default=list)
    cv_path = db.Column(db.String(200), nullable=True)