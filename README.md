# 🧠 Social Engineering V2

<summary>A prototype web application built with FastAPI and Socket.IO, featuring a modern, responsive authentication system and a real-time admin dashboard for monitoring user activity.</summary>

> ⚠️ **Note:** This project is for educational and demonstration purposes only. It is not secure for production use.

## 🚀 Features Overview

### 🔐 User Features

- **Sign Up** (`/signup`): Create a new user account easily.
- **Login** (`/login`): A modern, Google-style responsive login page that:
  - Adjusts seamlessly between desktop (card layout) and mobile (single-column layout).
  - Provides a clean, minimalist, and user-friendly interface.

### 🧑‍💼 Admin Features

- **Admin Login** (`/admin/login`):
  - Protected by an environment variable `ADMIN_SECRET`.
  - Only admins with the correct secret can access the dashboard.
- **Admin Dashboard** (`/admin/dashboard`):  
  A single-page, dark-mode dashboard with a tabbed interface and real-time updates, featuring:

#### 🧍 Users Tab
- Displays all registered users and their (plaintext) passwords.
- Includes a live search bar for instant filtering.
- Auto-refreshes every 5 seconds using `/api/get_users`.
- Export data with a “Download CSV” button.

#### 🕒 Login Logs Tab
- Displays a static table of all login events since server startup.
- Provides a “Download CSV” button for exporting the complete log.

#### ⚡ Real-Time Stream Tab
- Connects to a Socket.IO feed.
- Displays new login events instantly (no refresh required).
- Includes subtle fade-in animations for live updates.

## 🧩 Technology Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| **Backend** | FastAPI, Python-SocketIO           |
| **Server**  | Uvicorn                            |
| **Frontend**| Jinja2 Templates                   |
| **Styling** | Bootstrap 5 + Bootstrap Icons + Google Sans font |

## 📂 Project Structure
```
.
├── main.py                    # The main FastAPI & Socket.IO application
├── templates/
│   ├── login.html             # Public user login page (responsive)
│   ├── signup.html            # Public user signup page
│   ├── admin_login.html       # Admin-only login page
│   └── admin_dashboard.html   # All-in-one admin dashboard
└── static/
└── (empty)                # For optional .css or .js files
```
## ⚙️ Setup & Installation

### 1️⃣ Prerequisites
- Python 3.8+
- pip (Python package installer)

### 2️⃣ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/K4LYAN/social-engineering-V2.git
cd social-engineering-V2
pip install "fastapi[all]" uvicorn python-socketio
````

## 3️⃣ Configuration (Admin Secret)
- Set an environment variable for the admin dashboard password:
###On Linux/macOS:
-bashexport ADMIN_SECRET="your_super_secret_password"
### On Windows (CMD):
- cmdset ADMIN_SECRET="your_super_secret_password"
- If no variable is set, the app defaults to the insecure password adminpass.
## ▶️ Running the Application
- Start the development server using Uvicorn:
```uvicorn main:sio_app --reload --port 8000```
## Access the app in your browser:
- 👉 http://127.0.0.1:8000
- 🌐 How to Use
- 🧑 User Pages

Sign Up: ```http://127.0.0.1:8000/signup ```
Login:```http://127.0.0.1:8000/login```

## 🧠 Admin Pages

### Visit
```http://127.0.0.1:8000/admin/login ```
Enter your ADMIN_SECRET password.
- Access the dashboard at ```http://127.0.0.1:8000/admin/dashboard```

### Testing Real-Time Features
- Open the admin dashboard in one browser tab.
- Log in as a user from another tab.
- Watch new login events appear instantly on the “Real-Time Stream” tab.

## ⚠️ Security Warning
This is a prototype/demo — not for production use.

- ❌ Insecure storage: All users and logs are stored in memory only.
- ❌ Plaintext passwords: For demonstration purposes only.
- ❌ No CSRF protection: Forms are not secured against CSRF attacks.

Use this project only for learning, prototyping, or academic purposes.
## 💡 Future Enhancements (Ideas)

- ✅ Replace in-memory storage with SQLite or PostgreSQL.
- ✅ Hash passwords securely (e.g., bcrypt or passlib).
- ✅ Add JWT-based authentication.
- ✅ Integrate a proper frontend build (React or Vue).
- ✅ Add WebSocket authentication & user sessions.

## 🧑‍💻 Author
Kalyan
GitHub: @K4LYAN
🪪 License
**This project is released under the MIT License.
Feel free to fork, modify, and experiment responsibly.**
