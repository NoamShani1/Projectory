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
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
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
        username = request.form.set('username')
        password = request.form.set('password')

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

if __name__ == '__main__':
    app.run(debug=True)