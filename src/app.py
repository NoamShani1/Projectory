import sys
import os
import json
import logging
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, url_for
from src import create_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from .models import User, db, Project

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

# Source: ChatGPT
# Prompt: Give me a route to handle upload and saving of projects
# Define the folder for storing uploaded project images
UPLOAD_FOLDER = 'static/uploads/projects'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure directory exists

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Source: ChatGPT
# Prompt: Give me a route to handle 
# and save CV uploads in my app.py
# Directory to save uploaded CVs
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Configure the SQLite database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "pass.db")}'
 # Using a local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead of tracking modifications
# Intializing user json file 
USER_DB = 'userpass.json'

# Initialize Flask-Migrate
migrate = Migrate(app, db)


# Automatically create tables before the first request if they don't exist
@app.before_request
def create_tables():
    db.create_all()
    initialize_users_from_json()  # Load users from JSON into the database
    
# Load users from the JSON file and insert them into the database (if needed)
def initialize_users_from_json():
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as file:
            try:
                users = json.load(file)  # Load JSON as a list of dictionaries
                for details in users:
                    if isinstance(details, dict):  # Ensure details is a dictionary
                        username = details.get('username', 'Unknown')  # Extract username
                        if not User.query.filter_by(username=username).first():
                            new_user = User(
                                username=username,
                                first_name=details.get('first_name', 'Unknown'),
                                last_name=details.get('last_name', 'Unknown'),
                                password=details.get('password', 'Unknown')
                            )
                            db.session.add(new_user)
                db.session.commit()
            except json.JSONDecodeError:
                logging.error("Failed to load users from JSON file.")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                
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

@app.route('/editprofile/<username>', methods=['GET'])
def edit_profile(username):
    user = User.query.filter_by(username=username).first()
    #if user:
    return render_template('editprofile.html', user=user)
    #else:
        #return jsonify({"error": "User not found"}), 404

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
        # Redirect to the specific user's profile page
        return redirect(url_for('profile_page', username=user.username))
    else:
        return jsonify({'message': 'Invalid username or password'})  # Return error message

@app.route('/search_user', methods=['GET'])
def search_user():
    username_query = request.args.get('username', '').strip()
    
    if not username_query:
        return jsonify({"error": "Username is required"}), 400

    # Perform case-insensitive substring search using ilike
    #matching_users = User.query.filter(User.username.ilike(f"%{username_query}%")).all()
    matching_users = User.query.filter(func.lower(User.username).like(f"%{username_query.lower()}%")).all()
    
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
    data = request.get_json()
    if not data or 'username' not in data or 'first_name' not in data:
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
    print("existing user check: ",existing_user)
    if existing_user:
        return jsonify({"error": f"User with username '{username}' already exists"}), 409

    # Add the new user to the database
    new_user = User(username=username, first_name=first_name, last_name=last_name, password=password)
    print("new user: ",new_user)
    db.session.add(new_user)
    db.session.commit()

    # Update the JSON file with the new user details
    update_json_file(username, first_name, last_name, password)

    # Redirect to the new user's profile page
    return redirect(url_for('profile_page', username=new_user.username))

def update_json_file(username, first_name, last_name, password):
    users = []

    # Load existing users from JSON if the file exists
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as file:
            try:
                data = json.load(file)
                
                # If the data is a dictionary, convert it to a list of dictionaries
                if isinstance(data, dict):
                    logging.warning("Converting dictionary to list of users.")
                    # Convert each key-value pair to a list of dictionaries
                    users = [{"username": v.get("username", ""),
                              "first_name": v.get("first_name", ""),
                              "last_name": v.get("last_name", ""),
                              "password": v.get("password", "")} 
                             for k, v in data.items()]
                elif isinstance(data, list):
                    users = data  # Data is already in the correct format
                else:
                    logging.warning("Unknown JSON structure. Reinitializing to empty list.")
                    users = []

            except json.JSONDecodeError:
                logging.error("Failed to load JSON file, initializing an empty list.")
                users = []

    # Check if the user already exists and update their details
    for user in users:
        if user.get("username") == username:
            user["first_name"] = first_name
            user["last_name"] = last_name
            user["password"] = password
            break
    else:
        # If the user does not exist, add them as a new entry
        users.append({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        })

    # Save the updated list back to the JSON file
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

# source: ChatGPT, prompt: give me routing to save and handle the upload of skills
# and CV upload 
# Route to save updated profile data
@app.route('/save_profile/<username>', methods=['POST'])
def save_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Save skills
    skills = request.form.getlist('skills[]')
    user.skills = skills  # Assuming user.skills is a list or can be processed appropriately

    # Save links
    links = request.form.getlist('links[]')
    user.links = links  # Assuming user.links can store this information

    # Save updated user information
    db.session.commit()

    # Redirect to the updated profile
    return redirect(url_for('profile_page', username=username))

# Route to handle the CV upload
@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    if 'cv' not in request.files:
        return jsonify({"error": "No file part"}), 400


    file = request.files['cv']
    username = request.form['username']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Update the user's CV path
        user = User.query.filter_by(username=username).first()
        if user:
            user.cv_path = save_path
            db.session.commit()
            return redirect(url_for('profile_page', username=username))
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Invalid file format. Only PDF files are allowed."}), 400

@app.route('/save_project/<username>', methods=['POST', 'GET'])
def save_project(username):
    #print(f"Debug: opens page")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get form data (no extra checks, just save input)
    project_title = request.form.get("project_title") or None
    project_description = request.form.get("project_description") or None
    #print(f"Debug: getting request forms for input")
    
    # Handle image upload 
    # file_path = None
    # if 'project_image' in request.files:
    #     file = request.files['project_image']
    #     if file.filename and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         file.save(file_path)
    #         file_path = f"uploads/projects/{filename}"  # Save relative path for static access
    #         print(f"Debug: able to upload")

    # Save new project in the database
    new_project = Project(
        user_id=user.id,
        title=project_title,
        description=project_description,
      #  image_path=file_path  # Can be None if no image uploaded
    )

    db.session.add(new_project)
    db.session.commit()

    return redirect(url_for('profile_page', username=username))

# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for easier troubleshooting