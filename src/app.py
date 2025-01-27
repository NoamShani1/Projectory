import sys
import os
import json
from src import __init__
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

USER_DB = 'userpass.json'

if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

#Load user database
@app.route('/')
def login_page():
    return render_template('login.html')

#authecation of user
@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with open(USER_DB, 'r') as f:
        users = json.load(f)
    if username in users and users[username] == password:
        return jsonify({'message': 'Login Successful!'})
    else:
        return jsonify({'message': 'Invalid username or password'})
    
#register user
@app.route('/register', methods = ['POST'])
def register(): 
    username = request.form.get('username')
    password = request.form.get('password')
    
    with open(USER_DB, 'r') as f:
        users = json.load(f)
    
    if username in users: 
        return jsonify({'message': 'User already exists'}), 400
    
    #Add a user
    users[username] = password
    
    #save back to JSON file
    with open(USER_DB, 'w') as f:
        json.dump(users, f)
        
    return jsonify({'message': 'User created successfully!'})

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Debug prints to verify the paths
print("Project root directory:", project_root)
print("Current sys.path:", sys.path)

print("create_app successfully imported:", __init__)

# Call the create_app function and run the application
app = __init__()

if __name__ == "__main__":
    app.run(debug=True)