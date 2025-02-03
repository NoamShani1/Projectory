import sys
import os
import json
import logging
import sqlite3
import database
from flask import Flask, jsonify, render_template, request
from __init__ import create_app  # Import the function to initialize the Flask app
from flask_sqlalchemy import SQLAlchemy

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask app using the create_app() function
app = create_app()

# Configure the SQLite database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userpass.db'  # Using a local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead of tracking modifications

# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)

# Define the User model to represent the 'users' table in the database
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(80), nullable=False)  # Username field (required)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email address (required)

# Automatically create tables before the first request if they don't exist
@app.before_request
def create_tables():
    db.create_all()

# Route to render the login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# Route to render the signup page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Route to search for users based on a query parameter
# @app.route('/search', methods=['GET'])
# def search_users():
#     query = request.args.get('q', '')  # Get the search query from URL parameters
#     if query:
#         # Perform case-insensitive search for matching usernames
#         results = User.query.filter(User.username.ilike(f"%{query}%")).all()
#         # Return the search results as a JSON list
#         return jsonify([{'id': user.id, 'username': user.username} for user in results])
#     return jsonify([])  # Return an empty list if no query is provided

# JSON-based file to store username-password mappings for basic authentication
USER_DB = 'userpass.json'

# Create an empty JSON file if it doesn't already exist
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

# Route to authenticate user login using data from the JSON file
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']  # Get the submitted username
    password = request.form['password']  # Get the submitted password
    # Read existing user data from the JSON file
    with open(USER_DB, 'r') as f:
        users = json.load(f)
    # Check if the provided username and password match the stored credentials
    if username in users and users[username] == password:
        return render_template('home_page.html')  # Redirect to the home page if authenticated
    else:
        return jsonify({'message': 'Invalid username or password'})  # Return an error message if authentication fails

@app.route('/search_user', methods=['GET'])
def search_user():
    username_query = request.args.get('username')
    if not username_query:
        return jsonify({"error": "Username is required"}), 400
    
    matching_users = search_users_in_db(username_query)
    if matching_users:
        return jsonify({"exists": True, "users": matching_users, "message": f"Found {len(matching_users)} users"})
    return jsonify({"exists": False, "message": "No matching users found"})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({"error": "Username is required"}), 400
    
    username = data['username']

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        conn.close()

        # Update the JSON file after adding the user
        update_json_from_db()

        return jsonify({"success": True, "message": f"User '{username}' added successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": f"User '{username}' already exists"}), 409

# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for easier troubleshooting
