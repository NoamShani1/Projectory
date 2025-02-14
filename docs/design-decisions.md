---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions - Projectory

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>

User Authentication

Profile Structure

Project Display & Sharing

Search Functionality

File Upload & CV Handling

User Deletion

</details>

## 01: User Authentication

### Meta

Status
: **Work in progress** - Decided 

Updated
: 01-02-2025

### Problem statement

Should we handle authentication manually or use Flask-Login for session management?

Our application is built with Flask and requires secure user authentication. Managing authentication manually would require handling session storage, security vulnerabilities, and password management, adding significant complexity to the project.

Therefore, we decided to use Flask-Login for session management, allowing efficient and secure handling of user authentication while reducing development overhead.

### Decision

Flask-Login was implemented to handle session management, ensuring that authentication and user sessions are secure and scalable.

### Regarded options
#### Criterion

Basic Session Handling
**Security**  Weak
**Ease of Use** | Manual 
**Scalabilitye** | Limited 

 Flask-Login 
 **Security**  Strong 
**Ease of Use** Automated
**Scalabilitye** Flexible |

---

## 2. Profile Structure

### Meta

Status
:  **Decided** 


### Problem statement

How should user profiles be structured to display key information while maintaining simplicity?

Profiles should allow users to present their skills, uploaded CVs, and project links. The design should be minimal yet informative to ensure easy navigation while showcasing relevant professional details.

Therefore, we structured profiles to include user information, project links, and downloadable CVs while ensuring that users can easily update their profiles.

### Decision

Profiles include usernames, skills, external links, and CV uploads. The profile page is structured with a sidebar for quick access to key user details.

*Decision was taken by:* Noam Shani

---



##  3. Project Display & Sharing

### Meta

Status
:  **Work in Progress** 


### Problem statement
How should projects be visually represented in a way that maximizes engagement and accessibility?

Projects should be easy to browse while maintaining a clean, visually appealing layout. Users should be able to upload project images and descriptions, making the platform functional for a variety of project types.

Therefore, we implemented a structured grid layout for project displays, allowing users to see a preview of multiple projects at once while keeping the interface clean and organized.

### Decision

A grid-based layout was implemented to balance visual appeal and content density while keeping project descriptions concise.

### Regarded options
#### Criterion

List View
**Visual Appeal**  Minimal
**Information Density** | High 
**Navigation** | Linear 

Grid View
**Visual Appeal**  Clean
**Information Density** | Balanced 
**Navigation** | Clear cut 

*Decision was taken by:* Noam Shani


---

## 4. Search Functionality

### Meta

Status
:  **Decided** 


### Problem statement
How should the search function? Does a user need to have an account in order to Search? 

User search should be intuitive, allowing users to find each other quickly. While ID-based search ensures uniqueness, it is not user-friendly. Username-based search provides a simpler and more natural way to look up profiles. No login should be required based on the Scope of the project and to ensure higher usability in a real-life scenario.

Therefore, we implemented username-based search to provide a more accessible and user-friendly experience.

### Decision

User search was built around usernames to facilitate ease of use and quick navigation.

### Regarded options
#### Criterion



ID-Based Search
**Usability**  lookup required 
**Search speed** | fast 
**Accessibility** | low 

Grid View
**Usability**  direct
**Search speed** | High 
**Accessibility** | high 

*Decision was taken by:* Noam Shani

---

## 6. User Deletion

### Meta

Status
:  **Decided** 


### Problem statement
Should users be allowed to delete their accounts, and how should this process be handled?

User deletion functionality is necessary to comply with privacy laws and user expectations. The system must ensure that deleting a user removes all related data securely while preventing accidental deletions.

Therefore, we implemented a deletion mechanism that removes user data from the database and also ensures that related entries in JSON files are updated accordingly.

### Decision

The /delete_profile/<username> route was added to allow users to be removed from the database and associated JSON storage. Proper checks ensure that deleted users no longer appear in the system.

### Regarded options
#### Criterion

Soft Delete
**Data Recovery**  Possible 
**Database Integrity** | Retains unused data 


Permanent Delete
**Data Recovery**  Irreversible 
**Database Integrity** | Clean

*Decision was taken by:* Noam Shani

