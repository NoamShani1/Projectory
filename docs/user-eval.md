---
title: User Evaluation
nav_order: 4
---

{: .label }
Noam Shani

{: .no_toc }
# User evaluation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>

User Registration & Onboarding

User Profile Management

User Deletion Experience
</details>

## 01: User Registration & Onboarding

### Meta

Status
: **Work in progress** 


### Goal

How long does it take users to register a new account, and what is the drop-out rate?

### Method

We tracked the time taken for users to complete the registration process and collected feedback on drop-out points. This was done through:

-  measuring the time between Signing up, form submission and registration confirmation.


### Results

Average registration time: 30 seconds.

Due to the extremly easy registration process and the forward nature of the account, we have no drop-out points or issues during this process. 

### Implications

We will implement the following changes to improve registration:

- Create more advanced password requirements and provide clearer guidance in order to better security.

- Add an email form-field and add confirmation to create a better 'real-life' application.


---

## 02:  User Profile Management

### Meta

Status
: **Work in progress** 


### Goal

How easily can users update their profile and add projects?

### Method

We observed users performing key profile update actions and recorded:

- The time taken to edit profile details.

- The number of users who successfully added a project.

- Issues encountered during the process.



### Results

Average time to update profile: 1 minute.

While uploading and editing profile information works without issues (including uploading links, skills, and CVs, as well as saving and modifying this information), I was unable to successfully implement the feature for securely uploading and handling project additions.

Although the logic and modeling were provided (as seen in the following GitHub branch: [addproject](https://github.com/NoamShani1/Projectory/tree/addproject)), I repeatedly encountered 500 errors, likely due to issues within the database, the initialization file, and the migration of new data to the database.

### Implications

To improve the app and resolve this issue in the future:

- Provide a clearer database structure and include the project model in earlier iterations.
- Improve image upload handling with clearer feedback.


---

## 02:  User Deletion Experience

### Meta

Status
: **Work in progress** 


### Goal

How intuitive is the account deletion process for users?


### Method

We tested the deletion feature and recorded:

- Time taken to locate and complete deletion.


### Results

Average time to update profile: 1 minute.

The process to delete an account is very clear and is visible under 'edit profile'. It requires one click and one confirmation. 


### Implications

We will improve the user deletion experience by:

- Adding a confirmation message explaining what will happen after deletion (e.g that account is permanently gone).

- alternativly provide an option for users to temporarily deactivate accounts instead of permanent deletion.