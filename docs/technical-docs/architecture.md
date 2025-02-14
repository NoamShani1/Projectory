---
title: Projectory Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
Noam Shani

{: .no_toc }
# Architecture


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Projectory is a Flask-based web application that enables students and freelancers to showcase their projects in a streamlined and accessible format. Unlike traditional CVs that limit applicants to static text, Projectory provides a simple, public-facing profile page where users can:

- Upload and display projects with descriptions and images
- List skills, links, and CVs for potential employers
- Be searchable by username, allowing recruiters to access their work without logging in

How does Projectory achieve this?
- The backend, built with Flask, manages user - authentication, project storage, and search functionalities.
- The frontend is dynamically generated using Jinja2 templating, ensuring that user data is seamlessly rendered into HTML pages.
- SQLite serves as the database, efficiently storing user accounts, project data, and uploaded content.
- A username-based search function allows quick profile discovery, eliminating unnecessary barriers for recruiters.

## Bird's Eye View
At its core, Projectory operates on a client-server architecture:

Client-Side (Frontend):

- Renders user interfaces using HTML and CSS.
- Employs JavaScript for interactivity and asynchronous operations.
- Utilizes Jinja2 templating to dynamically inject data into HTML templates.

Server-Side (Backend):

- Manages user authentication and session handling.
- Processes CRUD operations for user profiles and projects.
- Handles file uploads, including project images and CVs.
Interacts with the SQLite database to store and retrieve data.
- This separation ensures a clear distinction between presentation and business logic, promoting maintainability and scalability.

## Class Diagram

![Class Diagram](/Projectory/assets/images/class.png)

## Activity

![Activity](/Projectory/assets/images/activity.png)

## Use-Case Diagram

![Use Case Diagram](/Projectory/assets/images/usecase.png)


## Codemap

Projectory follows a modular Flask application structure, with clearly separated concerns for authentication, data management, and UI rendering.

#### Core Components
1. Application Entrypoint
app.py - Initializes the Flask application, registers blueprints, and defines the main routes for profile handling, project uploads, and search functionality.

2. Authentication & User Management
auth.py - Handles login & signup routes and connects user sessions.
models.py - Defines User and Project models, setting up relationships between them.
database.py - Manages SQLite interactions for user profiles and project storage.
1. Frontend (Templates & UI)
Jinja2 templates dynamically generate HTML pages from backend data.
Important templates:
- profile.html - Displays user information and uploaded projects.
- editprofile.html - Allows users to update their skills, links, and CV.
- addproject.html - Enables users to upload new projects with descriptions and images.
- search.html - Implements the username search feature.
1. Search & Public Access
- Homepage (frontpage.html) - Features a username-based search, enabling recruiters to find profiles.
- Search logic (app.py) - Queries the database and returns matching user profiles in search.html.
1. Configuration & Initialization
- config.py - Contains application settings, such as database paths and session configurations.
- __init__.py - Initializes Flask and registers the blueprints for modular routing.

## Cross-cutting concerns
This section explains how Projectory behaves internally, helping others understand key data flows, decision-making trade-offs, and state management.

### User Authentication & Session Management
##### Signup Behavior:

Users register with first name, last name, username, and password (signup.html).
The credentials are stored securely in the database (auth.py processes requests).

##### Login Behavior:

Users log in (login.html), and Flask stores session data to persist authentication.
After logging in, users are redirected to home_page.html, where they can manage their profiles.
Profile & Project Management
Profiles (profile.html) dynamically load user data via Jinja2 templating.

##### Each profile displays:

Username, name, skills, links, CVs, and projects.
Users can edit their skills and upload a CV from editprofile.html.
Projects are uploaded from addproject.html, with their data stored in SQLite.

##### Project Upload Process:

Users submit a title, description, and optional image.
Flask handles the form in app.py, storing project details in the database.
Images are saved as files, with paths stored in SQLite.
Search & Public Access Behavior

##### How Recruiters Find Users:

The search bar (frontpage.html) queries the database for matching usernames.
The results are displayed in search.html, linking directly to user profiles.

##### Why is Login Not Required for Viewing Profiles?

The system is designed to eliminate friction for recruiters, making profiles public by default.

##### Data Flow & State Management
Frontend-to-Backend Communication:

The frontend dynamically renders user data via Jinja2 templates.
Flask handles HTTP requests and processes form submissions.
The database stores user profiles and project data, retrieved on demand.

##### Session Persistence:

Flask session management maintains authentication across pages.
However, app state is not stored beyond user sessions, meaning real-time updates (e.g., AJAX, WebSockets) are not currently implemented.

##### Key Design Decisions
Minimalist Profile Pages

Focus on showcasing projects and skills, avoiding unnecessary features.
Unlike LinkedIn or Behance, the goal is clarity and simplicity.
Public Search Without Login Requirement


#####  SQLite for Lightweight Storage

Chosen for simplicity and local development.
