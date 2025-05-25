import uvicorn
from fastapi import FastAPI
from routes import index_routes, todo_routes, user_routes

app = FastAPI()
# app.include_router(index_routes)
# app.include_router(todo_routes)
app.include_router(user_routes)

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)
