from flask import Flask, request, render_template, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

#Path to the JSON file
USER_DB = 'userpass.json'

#Ensure the JSON file exists
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)  # Initialize with an empty JSON object
        
@app.route('/')
def frontpage():
    return render_template('frontpage.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login_', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Show login form

    username = request.form.get('username')
    password = request.form.get('password')

    # Load users from the JSON file
    with open(USER_DB, 'r') as f:   
        users = json.load(f)

    # Authenticate user
    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Load users from the JSON file
        with open(USER_DB, 'r') as f:
            users = json.load(f)

        if username in users:
            return jsonify({'message': 'Username already exists'}), 400
        

        # Save new user credentials
        users[username] = password

        with open(USER_DB, 'w') as f:
            json.dump(users, f)

        # Redirect to the login page
        return redirect(url_for('login_page'))
    
@app.route('/home_page')
def home_page():
    username = request.args.get('username')  # Retrieve username from query params
    
    # Load users from the JSON file
    with open(USER_DB, 'r') as f:
        users = json.load(f)

    if username in users:
        return render_template('home_page.html', username=username)
    else:
        return redirect(url_for('login_page'))
    
@app.route('/home', methods=['POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')

        # Load users from the JSON file
        with open(USER_DB, 'r') as f:
            users = json.load(f)

        # Ensure user exists in the database
        if username in users:
            user_data = users[username]

            # Extract skills, links, and CV (default to empty lists if not set)
            user_skills = user_data.get('skills', [])
            user_links = user_data.get('links', [])
            user_cv = user_data.get('cv', [])

            return render_template('home_page.html', username=username, skills=user_skills, links=user_links, cv=user_cv)
        
      
    
if __name__ == '__main__':
    app.run(debug=True)