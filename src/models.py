from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    skills = db.Column(db.PickleType, default=list)
    links = db.Column(db.PickleType, default=list)
    cv_path = db.Column(db.String(200), nullable=True)

    # Define the one-to-many relationship
    projects = db.relationship("Project", back_populates="user", cascade="all, delete")

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True)

    # Specify the foreign key relationship explicitly
    user = db.relationship("User", back_populates="projects", foreign_keys=[user_id])
