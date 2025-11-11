# social-engineering-V2

social-engineering-V2

A small educational demo showing insecure authentication patterns and an admin dashboard (for lab/training use only).

Important: This project is for learning and defensive purposes only. Do not use it to target real users or collect real credentials.

What’s inside

templates/ — login.html, signup.html, admin_login.html, admin_dashboard.html 

main.py — simple FastAPI + Socket.IO prototype (demo, stores data in-memory)

Quick start (local, isolated)
Create & activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

Install dependencies:
pip install fastapi uvicorn python-socketio jinja2 aiofiles

Run the app:
uvicorn main:sio_app --reload --port 8000

Open the site:
http://127.0.0.1:8000/login

Notes & safety
1.The code stores plaintext passwords and broadcasts login events for demonstration — this is intentionally insecure.
2.Use only synthetic test accounts in an isolated environment.
3.If you want, I can help convert this into a secure version (password hashing, remove sensitive logging, add CSRF/session protections).
 
