from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, models, database
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")  # ✅ fixed: must match actual route


# -------------------- Password Handling --------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# -------------------- JWT Token Handling --------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[schemas.TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return schemas.TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -------------------- Auth Dependency --------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)  # ✅ fixed: use get_db() generator, not SessionLocal()
):
    token_data = decode_access_token(token)
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
