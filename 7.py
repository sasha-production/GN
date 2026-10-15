from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import bcrypt
from pydantic import BaseModel
import uvicorn

# Настройки безопасности
SECRET_KEY = "super-secret-key-change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Имитация базы данных пользователей
users_db = {}

# Утилита для извлечения токена из заголовка Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Модели данных Pydantic
class UserRegister(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Вспомогательные функции ---

def hash_password(password: str) -> str:
    """Хеширование пароля."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка совпадения пароля с хешем."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Зависимость для проверки JWT и получения текущего пользователя."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jwt.PyJWTError:
        raise credentials_exception


# --- Маршруты (Эндпоинты) ---

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    """Маршрут для регистрации нового пользователя."""
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    users_db[user.username] = {
        "username": user.username,
        "password": hash_password(user.password)
    }
    return {"message": "Пользователь успешно зарегистрирован"}


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Маршрут для входа (генерация токена). Принимает form-data."""
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Неверное имя пользователя или пароль"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected-route")
def get_protected_data(username: str = Depends(get_current_user)):
    """Защищенный маршрут, доступный только с валидным JWT-токеном."""
    return {
        "message": "Вы получили доступ к защищенным данным!",
        "user": username
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
