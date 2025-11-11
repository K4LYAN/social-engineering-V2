# social-engineering-V2
This project is a prototype web application built with FastAPI and Socket.IO. It features a modern, responsive user authentication system and a comprehensive, real-time admin dashboard for monitoring user activity.

The application demonstrates:

1. Modern, responsive, mobile-first UI design for login pages.
2. A secure, single-page admin panel with a tabbed interface and data export.
3. Real-time updates using Socket.IO (for live login events).
4. Data polling for semi-real-time table updates (for the user list).
5. A clear separation of user and admin routes.

Features

1. User Features
/signup: A simple page to create a new user account.
/login: A modern, Google-style responsive login page that adapts perfectly to both desktop (card view) and mobile (single-column view).

2. Admin Features
/admin/login: A secure login page for administrators, protected by a secret password.
/admin/dashboard: A single-page, consolidated dashboard with a modern dark-mode UI, icons, and three tabs:

Users Tab:
1. Displays a list of all registered users and their passwords.
2. Features a live search bar to filter the list instantly.
3. Auto-refreshes the user list every 5 seconds by polling the /api/get_users endpoint.
4. Includes a "Download CSV" button to export the current user list.

Login Logs Tab:

Shows a static table of all login events captured since the server started.
Includes a "Download CSV" button to export the complete log history.

Real-time Stream Tab:

Connects to a Socket.IO feed.
Instantly displays new login events as they happen with a subtle fade-in animation, without needing a page refresh.

Technology Stack:

Backend: FastAPI

Real-time: Python-SocketIO

Server: Uvicorn

Frontend: Jinja2 Templates

Styling: Bootstrap 5 (with Bootstrap Icons and Google Sans font)

Project Structure
.
├── main.py             # The main FastAPI & Socket.IO application
├── templates/
│   ├── login.html      # Public user login page (responsive)
│   ├── signup.html     # Public user signup page
│   ├── admin_login.html # Admin-only login page
│   └── admin_dashboard.html # All-in-one admin panel
└── static/
    └── (empty)         # For any .css or .js files


Setup and Running

1. Prerequisites

Python 3.8+

pip (Python package installer)

2. Installation

Clone this repository or save the files in a project directory.

Install the required Python packages:

pip install "fastapi[all]" uvicorn python-socketio


3. Configuration (Admin Password)

The admin dashboard is protected by a secret password. For security, set this as an environment variable before running the server.

Linux/macOS:

export ADMIN_SECRET="your_super_secret_password"


Windows (CMD):

set ADMIN_SECRET="your_super_secret_password"


If no variable is set, the app will default to the insecure password "adminpass".

4. Running the Application

Use uvicorn to run the sio_app (Socket.IO + FastAPI) object from main.py:

uvicorn main:sio_app --reload --port 8000


The server will be available at http://127.0.0.1:8000.

How to Use

User Pages

Sign Up: http://127.0.0.1:8000/signup

Log In: http://127.0.0.1:8000/login

Admin Dashboard

Go to http://127.0.0.1:8000/admin/login.

Enter the ADMIN_SECRET password you set in the configuration.

You will be redirected to the main dashboard at http://127.0.0.1:8000/admin/dashboard.

To test the real-time features, open the admin dashboard and then, in a separate browser window, log in as a user. You will see the new login event appear instantly on the "Real-time Stream" tab.

⚠️ Security Warning

This is a prototype application. It is NOT secure for production use.

In-Memory Storage: All users and login events are stored in Python variables and will be lost when the server restarts.

Plaintext Passwords: Passwords are intentionally stored and displayed as plaintext for demonstration purposes. Never do this in a real application.

No CSRF Protection: The forms do not have Cross-Site Request Forgery protection.
