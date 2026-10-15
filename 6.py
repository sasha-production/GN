from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uvicorn

app = FastAPI(title="User API")


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


users_db: List[User] = []
next_id: int = 1


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    global next_id
    user = User(id=next_id, name=payload.name, email=payload.email)
    users_db.append(user)
    next_id += 1
    return user


@app.get("/users", response_model=List[User])
def get_users():
    return users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserUpdate):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            updated = user.model_copy(
                update=payload.model_dump(exclude_unset=True)
            )
            users_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
