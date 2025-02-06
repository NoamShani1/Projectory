import sqlite3
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = "pass.db"
JSON_FILE = "userpass.json"  # Using userpass.json for JSON storage


# Source: ChatGPT
# Prompt: "Write a Flask application that connects to an SQLite database. 
# The database should contain a table of users with usernames. 
# mplement an endpoint /search_user that takes a GET parameter called username and 
# searches for users whose usernames match the query using a LIKE SQL statement. 
# Return a JSON response indicating whether any users were found, 
# along with the list of matching usernames if any. Use a simple database file named pass.db.'


# Function to load users from a JSON file
def load_users_from_json():
    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# Function to save users to the JSON file
def save_users_to_json(users):
    with open(JSON_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Function to initialize the SQLite database and sync with the JSON file
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()


    # Load users from the JSON file and insert them into the database
    users = load_users_from_json()
    for user in users:
        cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (user,))
    
    conn.commit()
    conn.close()



if __name__ == '__main__':
    # Initialize the database and populate it with data from the JSON file
    initialize_database()
    app.run(debug=True, port=5001)
