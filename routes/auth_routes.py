from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import jwt

users_db = {}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None or email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return users_db[email]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/api/register", response_model=UserOut)
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = {"email": user.email, "password": user.password}
    return {"email": user.email}

@router.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    response.set_cookie(key="jwt", value=token, httponly=True, samesite="lax")
    return {"message": "Login successful"}

@router.get("/api/profile", response_model=UserOut)
def profile(jwt: Optional[str] = Cookie(None)):
    if not jwt:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = verify_token(jwt)
    return {"email": user["email"]}