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

    # Create the users table if it does not exist
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS users (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         username TEXT UNIQUE NOT NULL
    #     )
    # ''')

    # Load users from the JSON file and insert them into the database
    users = load_users_from_json()
    for user in users:
        cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (user,))
    
    conn.commit()
    conn.close()

# Function to fetch all users from the database and save them to the JSON file
def update_json_from_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users')
    users = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Save users to JSON
    save_users_to_json(users)

# Function to search for users in the database
def search_users_in_db(query):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return [user[0] for user in results]

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

if __name__ == '__main__':
    # Initialize the database and populate it with data from the JSON file
    initialize_database()
    app.run(debug=True, port=5001)
