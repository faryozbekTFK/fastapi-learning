from fastapi import APIRouter

router = APIRouter(prefix="/todo", tags=["todo"])


@router.post('/')
async def create_todo(todo):
    return {"message": "Todo created", "todo": todo}


@router.get('/')
async def get_todos():
    return {"message": "List of todos"}


@router.get('/{todo_id}')
async def get_todo(todo_id: int):
    return {"message": "Todo details", "todo_id": todo_id}


@router.put('/{todo_id}')
async def update_todo(todo_id: int, todo):
    return {"message": "Todo updated", "todo_id": todo_id, "todo": todo}


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int):
    return {"message": "Todo deleted", "todo_id": todo_id}


@router.delete('/')
async def delete_all_todos():
    return {"message": "All todos deleted"}
