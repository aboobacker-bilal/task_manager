# Task Management Application

## Project Overview

A role-based Task Management system built with Django and Django REST Framework. This application supports role-specific features, JWT authentication, and user task reporting including worked hours.

## Features

### Authentication
- Secure JWT-based login system.
- Authenticated users receive an access and refresh token.

### Roles & Permissions
- **SuperAdmin**
  - Manage Admins (create, delete, promote/demote).
  - Manage Users (create, delete, update).
  - Assign users to Admins.
  - View and manage all tasks and completion reports.

- **Admin**
  - Create, assign, and manage tasks.
  - View task completion reports of assigned users.
  - Cannot manage users.

- **User**
  - View assigned tasks.
  - Mark tasks as completed with a completion report and worked hours.

---

## Technologies Used

- Python 3.10+
- Django
- Django REST Framework
- JWT (via `djangorestframework-simplejwt`)
- SQLite

---

## API Endpoints

### **1. Get All Tasks**

**Request:**

```
GET /api/tasks/
Authorization: Bearer <access_token>
```

**Response:**

```
{
    "id": 2,
    "title": "optimize the  code",
    "description": "Optimize SMS and OTP sending code for speed and maintainability",
    "due_date": "2025-04-24",
    "status": "completed",
    "completion_report": "optimized the code",
    "worked_hours": 6.0,
    "assigned_to": 2
},
{
    "id": 3,
    "title": "Attribute error",
    "description": "Encountering an AttributeError during SMS and OTP sending.",
    "due_date": "2025-04-21",
    "status": "completed",
    "completion_report": "Resolved AttributeError causing 403 during SMS and OTP sending by fixing attribute access and ensuring proper authentication",
    "worked_hours": 2.0,
    "assigned_to": 3
}
```

### **2. Update Task Status with Completion Report**

**Request:**

```
PUT /api/tasks/{task_id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response:**

```
{
    "status": "completed",
    "completion_report": "Resolved AttributeError causing 403 during SMS and OTP sending by fixing attribute access and ensuring proper authentication",
    "worked_hours": 2.0
}
```

### **3. View Completion Report for a Task**

**Request:**

```
GET /api/tasks/{task_id}/report/
Authorization: Bearer <access_token>
```

**Response:**

```

{
    "status": "completed",
    "completion_report": "Resolved AttributeError causing 403 during SMS and OTP sending by fixing attribute access and ensuring proper authentication",
    "worked_hours": 2.0
}
```

---

## Local Setup Instructions

### Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/aboobacker-bilal/task_manager.git
cd task_manager
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```
---

This project is open source.