# Employee Management System

## Introduction

This project is a Django-based Employee Management System. It provides functionalities to manage employees, departments, companies, and more within the system.

## Project Structure

employee_management/
│
├── debug.log
├── manage.py
├── app/
│ ├── admin.py
│ ├── apps.py
│ ├── decorators.py
│ ├── migrations/
│ ├── models.py
│ ├── permissions.py
│ ├── serializers.py
│ ├── urls.py
│ └── views.py
└── employee_management/
├── init.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py

### Prerequisites

- Python 3.10+
- Django 4.x

### Installation

1. Clone the repository:

   ```
   git clone <repository_url>
   cd employee_management
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```
   python manage.py migrate
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage Instructions

- Access the application at `http://127.0.0.1:8000/`
- Use the provided endpoints to manage employees, departments, and companies.

## Registration

- For security reasons, users should only be created through the django admin panel.
- Create users through the Django admin panel, after running the application with python manage.py runserver, you have to create a superuser
- python manage.py createsuperuser
- Then head to `http://127.0.0.1:8000/admin`
- Login and add user and choose the role and use it to login

### Endpoints

You'll find all the API Endpoints in test.http file in the app directory, ready to get tested through Rest Client extension

## Completion Summary:

Completed backend models with validations and security through token authentication.
Implemented APIs for CRUD operations on all models.
Implemented logging with debug.log and debugging messages.

## Users and Roles

Only users with admin role can create/update Companies
Only users with manager role can create/update employees

## Backend Implementation in details:

Models
Implemented models for User Accounts, Company, Department, and Employee with appropriate fields and relationships.
Validations & Business Logic
Implemented validations to ensure all required fields are filled.
Validated email addresses and mobile numbers for correct format.
Implemented automatic calculations for the number of departments, employees in the company, employees in the department, and days employed.
Ensured that the Department field in the Employee model only accepts departments related to the selected company.
Handled cascading deletions to manage related records properly or prevent deletion if necessary.
Implemented error handling with appropriate error codes and messages.
Security & Permissions
Implemented token-based authentication to secure access to data.
Implemented role-based access control to restrict data access based on user roles (e.g., Admin, Manager, Employee).
APIs
Created RESTful APIs for CRUD operations on Company, Department, and Employee models.
Ensured secure handling of data in API operations.
Followed RESTful conventions in API design, including proper HTTP methods.
Provided clear documentation on API endpoints, parameters, and expected responses.
Logging
Implemented logging to track application behavior and capture errors.
Ensured logs contain sufficient detail for troubleshooting issues while protecting sensitive information.
