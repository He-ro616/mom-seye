import os
import json
import hashlib
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Serve static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Configure the OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

API_KEY = os.getenv("API_KEY")

@app.get("/api/users")
async def get_all_users(request: Request):
    if request.headers.get("X-API-Key") == API_KEY:
        return JSONResponse(content=load_users())
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})

# Default credentials
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_user(username):
    users = load_users()
    return users.get(username)

def add_user(username, password):
    users = load_users()
    if username in users:
        return False  # User already exists
    # In a real application, you should hash the password
    users[username] = {"password": password} # For simplicity, storing as plain text
    save_users(users)
    return True

class ChatMessage(BaseModel):
    message: str
    history: list[dict]

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...), parent_name: str = Form(...), child_name: str = Form(...), child_dob: str = Form(...), phone_number: str = Form(...)):
    if add_user(username, password):
        response = RedirectResponse(url="/", status_code=303)
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if user and user["password"] == password:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="session", value="authenticated")
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if request.cookies.get("session") == "authenticated":
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session")
    return response

# --- Chat endpoint ---

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        # Read system prompt from file
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # Construct messages from history and new message
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        for message in chat_message.history:
            messages.append(message)
        messages.append({"role": "user", "content": chat_message.message})

        # Call OpenAI chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Access the content correctly in new API
        ai_message = response.choices[0].message.content

        # Append AI message to history
        chat_message.history.append({"role": "user", "content": chat_message.message})
        chat_message.history.append({"role": "assistant", "content": ai_message})

        return {"message": ai_message, "history": chat_message.history}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error: {str(e)}"}
        )
