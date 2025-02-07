import sys
import os
import json
import logging
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, url_for
from __init__ import create_app  # Import the function to initialize the Flask app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask app using the create_app() function
app = create_app()

basedir = os.path.abspath(os.path.dirname(__file__))

# Set up the database folder and file
db_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "database")
if not os.path.exists(db_folder):
    os.makedirs(db_folder)  # Create the database folder if it doesn't exist

db_file = os.path.join(db_folder, "pass.db")

# Configure the SQLite database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "pass.db")}'
 # Using a local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead of tracking modifications
# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)
# Intializing user json file 
USER_DB = 'userpass.json'

# Define the User model to represent the 'users' table in the database
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(80), nullable=False)  # Username field (required)
    first_name = db.Column(db.String(80), nullable=False)  # First Name
    last_name = db.Column(db.String(80), nullable=False)  # Last Name
    password = db.Column(db.String(80), nullable=False)  # Password (added)


# Automatically create tables before the first request if they don't exist
@app.before_request
def create_tables():
    db.create_all()
    
# Load users from the JSON file and insert them into the database (if needed)
def initialize_users_from_json():
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as file:
            try:
                users = json.load(file)
                for username, details in users.items():
                    if not User.query.filter_by(username=username).first():
                        new_user = User(
                            username=details.get('username', 'Unknown'),
                            first_name=details.get('first_name', 'Unknown'),
                            last_name=details.get('last_name', 'Unknown'),
                            password=details.get('password', 'Unknown')
                        )
                        db.session.add(new_user)
                db.session.commit()
            except json.JSONDecodeError:
                logging.error("Failed to load users from JSON file.")
                
# Route to render the login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# Route to render the signup page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Route to render the search page
@app.route('/search')
def search_page():
    return render_template('search.html')



# Create an empty JSON file if it doesn't already exist
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

# Route to authenticate user login using data from the JSON file
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']  # Get the submitted username
    password = request.form['password']  # Get the submitted password
   # Query the user from the database
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return render_template('home_page.html')  # Redirect if password matches
    else:
        return jsonify({'message': 'Invalid username or password'})  # Return error message

# Route to search for users by username (case-insensitive partial match)
# @app.route('/search_user', methods=['GET'])
# def search_user():
#     username_query = request.args.get('username', '')
#     if not username_query:
#         return jsonify({"error": "Username is required"}), 400

#     # Perform case-insensitive search using SQLAlchemy's ilike function
#     matching_users = User.query.filter(User.username.ilike(f"%{username_query}%")).all()
@app.route('/search_user', methods=['GET'])
def search_user():
    username_query = request.args.get('username', '').strip()
    
    if not username_query:
        return jsonify({"error": "Username is required"}), 400

    # Perform case-insensitive substring search using ilike
    #matching_users = User.query.filter(User.username.ilike(f"%{username_query}%")).all()
    matching_users = User.query.filter(func.lower(User.username).like(f"%{username_query.lower()}%")).all()
    

    # if matching_users:
    #     return jsonify({
    #         "exists": True,
    #         "users": [{"id": user.id, "username": user.username} for user in matching_users]
    #     })
    
    # return jsonify({"exists": False, "message": "No matching users found"})


    if matching_users:
        return jsonify({
            "exists": True,
            "users": [{"id": user.id, "username": user.username} for user in matching_users],
            "message": f"Found {len(matching_users)} user(s)" #need to change this to showing list of user profile
        })
    return jsonify({"exists": False, "message": "No matching users found"})


# Route to add a new user and redirect to their profile page
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'username' not in data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({"error": "Username, First Name, and Last Name are required"}), 400

    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": f"User with username '{username}' already exists"}), 409

    # Add the new user to the database
    new_user = User(username=username, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    # Update the JSON file with the new user and a default password
    update_json_file(username, first_name, last_name, password)

    # Redirect to the new user's profile page
    return redirect(url_for('profile_page', username=new_user.username))

# Route to register a new user from the sign-up form
@app.route('/register', methods=['POST'])
def register_user():
    # Get form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    password = request.form['password']

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": f"User with username '{username}' already exists"}), 409

    # Add the new user to the database
    new_user = User(username=username, first_name=first_name, last_name=last_name, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Update the JSON file with the new user details
    update_json_file(username, first_name, last_name, password)

    # Redirect to the new user's profile page
    return redirect(url_for('profile_page', username=new_user.username))

# Function to update the JSON file with new user-password pairs
def update_json_file(username, first_name, last_name, password):
    users = {}
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as file:
            users = json.load(file)

    # Add or update the user in the JSON file
    users[username] = {
        "first_name": first_name,
        "last_name": last_name,
        "password": password
    }

    with open(USER_DB, 'w') as file:
        json.dump(users, file, indent=4)
# Route to display the profile page for a specific user
@app.route('/profile/<username>', methods=['GET'])
def profile_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('profile.html', user=user)
    else:
        return jsonify({"error": "User not found"}), 404



# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for easier troubleshooting