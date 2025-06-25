from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

fake_users_db = {}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

class User(BaseModel):
    email: EmailStr
    hashed_password: str

class UserIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(email: str):
    user = fake_users_db.get(email)
    if user:
        return User(**user)
    return None

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", status_code=201)
def register(user_in: UserIn):
    if user_in.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_in.password)
    fake_users_db[user_in.email] = {"email": user_in.email, "hashed_password": hashed_password}
    return {"msg": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}