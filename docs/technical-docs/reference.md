---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
Noam Shani

{: .no_toc }
# Reference documentation



<details open markdown="block">
{: .text-delta }
Authentication Routes
GET /login
POST /login
GET /signup
POST /register

User Management Routes
GET /profile/<username>
POST /save_profile/<username>
POST /upload_cv
POST /delete_profile/<username>

Project Management Routes
POST /save_project/<username>

Search & Public Access Routes
GET /search_user
GET /search

Database Initialization & Utilities
@before_request create_tables()
initialize_users_from_json()
update_json_file()

<summary>Table of contents</summary>

## Overview
This document provides a structured reference for all routes, functions, and API endpoints used in the Projectory application.

Projectory is built using Flask and manages user data and projects through SQLite with SQLAlchemy ORM. The system supports user authentication, profile management, project handling, and public search access.
</details>

## Authentication Routes
### GET / Login

**Route:** `GET /login`

**Methods:** `GET`  

**Purpose:**  Displays the login page where users can enter their credentials.

**Sample output:**

Renders login.html

![Log in](/Projectory/assets/images/login.png)

#### POST /login

**Route:** `POST /login`

**Methods:** `POST`  

**Purpose:**  Authenticates user credentials and redirects to their profile if valid.

**Sample output:**

Response:
Success: Redirects to /profile/johndoe
Failure: Returns { "message": "Invalid username or password" }

In case of success, Renders profile.html

![profile](/Projectory/assets/images/profile.png)

### GET /signup

**Route:** `/signup`

**Methods:** `GET`  

**Purpose:**  Displays the signup page where users can create an account.

**Sample output:**
Renders signup.html

![Sign up](/Projectory/assets/images/signup.png)

### POST /register

**Route:** `/register`

**Methods:** `POST`  

**Purpose:**  Registers a new user and redirects them to their profile.

**Sample output:**

Sample Response:

Success: Redirects to /profile/johndoe
Failure: Returns { "error": "User with username 'johndoe' already exists" }



---


## 2. User Management Routes

### `GET /profile/<username>`

**Route:** `/profile/<username>`

**Methods:** `GET`

**Purpose:** Displays a user's profile page with their skills, projects, and CV.

**Sample output:**

Sample Output:

Renders profile.html
If the user is not found:

{ "error": "User not found" }


---

### `GET /editprofile/<username>`

**Route:** `/editprofile/<username>`

**Methods:** `GET`

**Purpose:** Allows a user to edit their profile information (skills, links, CV, etc.).


**Sample output:**

Renders editprofile.html

![Edit](/Projectory/assets/images/edit.png)

---

### `POST /save_profile/<username>`

**Route:** `/save_profile/<username>`

**Methods:** `POST`

**Purpose:** Saves updated skills and links to a users profile.

**Sample output:**

Sample Response:

Success: Redirects to /profile/johndoe
Failure: Returns { "error": "User not found" }


---

### `POST /upload_cv`

**Route:** `/upload_cv`

**Methods:** `POST`

**Purpose:** Handles CV uploads for user profiles.

**Sample output:**

Sample Response:

Success: Redirects to /profile/johndoe
Failure: Returns { "error": "Invalid file format. Only PDF files are allowed." }


---

### `POST /delete_profile/<username`

**Route:** `/delete_profile/<username>`

**Methods:** `POST`

**Purpose:** Deletes a user profile, removing their data from the database and userpass.json.

**Sample output:**
Sample Request: 
POST /delete_profile/johndoe
Sample Response:
Success: Redirects to /login
Failure: Returns { "error": "User not found" }
---

## 3. Project Management Routes

### `POST /save_project/<username>`

**Route:** `/save_project/<username>`

**Methods:** `POST`

**Purpose:** Allows a user to add a new project to their profile.

**Sample output:**

Sample Response:

Success: Redirects to /profile/johndoe
Failure: Returns { "error": "User not found" }

---


## 4. Search & Public Access Routes

### `GET /search_user`

**Route:** `/search_user`

**Methods:** `GET`

**Purpose:** Searches for users based on username input.

**Sample output:**
Sample Request:

GET /search_user?username=john

Sample Response:
{
  "exists": true,
  "users": [
    { "id": 1, "username": "johndoe" },
    { "id": 2, "username": "johnsmith" }
  ],
  "message": "Found 2 user(s)"
}

If no users are found:

{ "exists": false, "message": "No matching users found" }



---

### `GET /search`

**Route:** `/search`

**Methods:** `POST`

**Purpose:** Purpose: Displays the search page where users can look for profiles.


**Sample output:**
Sample Output:

Renders search.html

![Search](/Projectory/assets/images/search.png)

---

## 5. User Registration & Utilities



### `POST /add_user`

**Route:** `/add_user`

**Methods:** `POST`

**Purpose:** Purpose: Adds a new user via JSON request and redirects to their profile.


**Sample output:**

Success: Redirects to /profile/johndoe
Failure: { "error": "User with username 'johndoe' already exists" }

![Search](/Projectory/assets/images/search.png)


### `@before_request create_tables()`

**Purpose:** Ensures database tables are created before the first request.

### `initialize_users_from_json()`

**Purpose:** Loads users from userpass.json into the database if they dont already exist.

### `update_json_file()`

**Purpose:** Updates the JSON file with new user data when a user registers.

