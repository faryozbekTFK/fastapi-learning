from fastapi import FastAPI, Query, Path, Form, UploadFile, File
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


# class UserTypes(str, Enum):
#     admin = 'admin'
#     superuser = 'superuser'
#     normal = 'normal'


class UserImage(BaseModel):
    url: HttpUrl
    name: str


class User(BaseModel):
    id: int | None = None
    name: str
    age: int = Field(gt=15, le=65, description="Age must be between 15 and 65")
    email: str
    image: list[UserImage] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "age": 30,
                    "email": "johndoe@example.com",
                    "image": "https://example.com/image.jpg",
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "age": 25,
                    "email": "janesmith@example.com",
                    "image": None,
                },
            ]
        }
    }


# @app.get("/{keyword}")
# async def index(keyword: Annotated[str | None, Path(description='Nimadir'), ], search: str = Query(None, min_length=3, max_length=50, openapi_examples={"example1": {"value": "example"}, "example2": {"value": "test"}})):
#     return {"message": "Hello World"}


# @app.get('/user/{user_type}')
# async def get_user_type(user_type: UserTypes):
#     return {"user_type": user_type}


@app.post("/user", description='Body parametlar bilan ishlash')
async def create_user(user: User):
    return user


@app.put("/user/{user_id}", description='Query, Path va Body parametlar bilan bor vaqta ishlash')
async def update_user(
    user_id: Annotated[int, Path(gt=15, le=65)],
    user: User,
    search: str | None = Query(None, min_length=3, max_length=50),
):
    if user.name.find(search) != -1:
        return {"user_id": user_id, **user.dict()}
    else:
        return {"error": "Search term not found in name"}


@app.post("/create-account", description='Form bilan ishlash')
async def create_account(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    email: Annotated[str, Form(
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$")],
    image: Annotated[UploadFile, File()],
):
    return {
        "message": "Account created successfully",
        "data": {"username": username, "password": password, "email": email,  "image_size": image.size,
                 "image_type": image.content_type,
                 "image_filename": image.filename, },

    }
