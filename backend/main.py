from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Спецназ 22")

app.add_middleware(SessionMiddleware, secret_key="specnaz22-development-secret")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

USERS = {
    "admin": {"password": "admin", "role": "admin", "name": "Администратор"},
    "manager": {"password": "manager", "role": "manager", "name": "Руководитель"},
    "operator": {"password": "operator", "role": "operator", "name": "Оператор"},
}

ROLE_PERMISSIONS = {
    "operator": ["home", "production", "products", "history", "profile"],
    "manager": ["home", "production", "products", "history", "operators", "salary", "analytics", "profile"],
    "admin": ["home", "production", "products", "history", "operators", "salary", "analytics", "audit", "settings", "profile"],
}

@app.get("/")
async def login_page(request: Request):
    if request.session.get("username"):
        return RedirectResponse("/app", status_code=303)
    return FileResponse(FRONTEND_DIR / "login.html")

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = USERS.get(username)
    if not user or user["password"] != password:
        return RedirectResponse("/?error=1", status_code=303)
    request.session["username"] = username
    request.session["name"] = user["name"]
    request.session["role"] = user["role"]
    return RedirectResponse("/app", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@app.get("/app")
async def application(request: Request):
    if not request.session.get("username"):
        return RedirectResponse("/", status_code=303)
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/api/me")
async def current_user(request: Request):
    username = request.session.get("username")
    if not username:
        return JSONResponse({"authenticated": False}, status_code=401)
    role = request.session.get("role")
    return {
        "authenticated": True,
        "username": username,
        "name": request.session.get("name"),
        "role": role,
        "permissions": ROLE_PERMISSIONS.get(role, []),
    }
