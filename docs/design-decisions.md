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

Security Considerations
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
| Criterion | Basic Session Handling| Flask-Login |
| --- | --- | --- |
| **Security** | Weak | Strong |
| **Ease of Use** | Manual | Automated |
| **Scalabilitye** | Limited | Flexible |


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