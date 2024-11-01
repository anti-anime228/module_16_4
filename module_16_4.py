from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel


new_app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@new_app.get("/")
async def get_main_page() -> dict:
    return {"message": "Главная страница"}
# http://127.0.0.1:8000/

@new_app.get("/user/admin")
async def admin_panel() -> dict:
    return {"message": "Вы вошли как администратор"}
# http://127.0.0.1:8000/user/admin



@new_app.get("/users")
async def get_users() -> list[User]:
    return users


@new_app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: int = Path(ge=18, le=120, description='Enter age', example=24)
) -> str:
    if len(users) == 0:
        user = User(id=1, username=username, age=age)
        users.append(user)
    else:
        id = len(users) + 1
        user = User(id=id, username=username, age=age)
        users.append(user)

    return f"User {username} is registered"


@new_app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404,detail="User was not found")




@new_app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> User:
    for i in range(len(users)):
        if users[i].id == user_id:
            return users.pop(i)
    else:
        raise HTTPException(status_code=404, detail='User was not found')
