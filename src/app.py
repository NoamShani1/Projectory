import sys
import os
import json
import logging
from flask import Flask, jsonify, render_template, request
from __init__ import create_app  # Import the function properly
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG)

app = create_app()  # Call create_app() to initialize Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userpass.db'  # SQLite Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.before_request
def create_tables():
    db.create_all()  # Automatically create tables on first request

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Search route
@app.route('/search', methods=['GET'])
def search_users():
    query = request.args.get('q', '')
    if query:
        # Search for users with partial matches on the username (case-insensitive)
        results = User.query.filter(User.username.ilike(f"%{query}%")).all()
        return jsonify([{'id': user.id, 'username': user.username} for user in results])
    return jsonify([])

USER_DB = 'userpass.json'

if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

#authecation of user
@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with open(USER_DB, 'r') as f:
        users = json.load(f)
    if username in users and users[username] == password:
        return render_template('home_page.html')
    else:
        return jsonify({'message': 'Invalid username or password'})
    

if __name__ == "__main__":
    app.run(debug=True)
