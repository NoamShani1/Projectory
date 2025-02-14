---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
Noam Shani

{: .no_toc }
# Data model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

#### Projectory uses Flask-SQLAlchemy to manage its database. The schema consists of two main models:

- User Model (User) - Stores user authentication data, skills, links, and uploaded CVs.
- Project Model (Project) - Stores projects linked to users, including title, description, and an optional image.
  
### Entity Relationship Diagram (ERD)
View the Entity Relationship Diagram below for further understanding of both models:

![ERD](/Projectory/assets/images/ERD.png)

## Model Descriptions 

#### User Model (User)
The User model stores profile information, authentication credentials, and related data.

#### Schema as reference: 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    skills = db.Column(db.PickleType, default=list)
    links = db.Column(db.PickleType, default=list)
    cv_path = db.Column(db.String(200), nullable=True)

    projects = db.relationship("Project", back_populates="user", cascade="all, delete")

#### Behavior & Constraints:
- Each user has a unique username and authentication password.
- Skills and links are stored as PickleType fields, meaning they are stored as Python lists in the database.
- The cv_path field stores the path to an uploaded CV (if available).
- One-to-Many Relationship: A user can have multiple projects.


#### Project Model (Project)
The Project model stores information about user-created projects.

#### Schema as reference: 
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True)

    user = db.relationship("User", back_populates="projects", foreign_keys=[user_id])

#### Behavior & Constraints:
- Each project is linked to a single user (user_id is a foreign key).
- Projects can have a title, description, and optional image upload.
- Deleting a user will also delete all their projects (cascade="all, delete").


### File Upload Handling
- CVs: The cv_path in User stores the file path of an uploaded CV.
- Project Images: The image_path in Project stores uploaded project images.
- Uploaded files are stored on the server, with their paths saved in the database

### Summary of Relationships
- One-to-Many (1:N) Relationship:
- A User can have multiple Projects.
- Skills and links are stored within the User model rather than as separate tables.