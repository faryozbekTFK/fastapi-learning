from fastapi import APIRouter, HTTPException
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from database.db_connection import get_connection, release_connection
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["user"])


class User(BaseModel):
    first_name: str
    last_name: str
    email: str = None
    password: str


class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    password: str = None


@router.post('')
async def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, password) VALUES(%s, %s, %s, %s) RETURNING id, first_name, last_name, email',
            (user.first_name, user.last_name, user.email, user.password)
        )
        conn.commit()
        new_user = cursor.fetchone()
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400, detail="User already exists or invalid data")
    finally:
        cursor.close()
        release_connection(conn)

    return new_user


@router.put('/{user_id}')
async def update_user(user_id: int, user: UserUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.close()
        release_connection(conn)
        raise HTTPException(
            status_code=404, detail=f"User not found {user_id}")

    updating_user = user.dict(exclude_unset=True)
    query_str = ", ".join([f"{field} = %s" for field in updating_user.keys()])

    query = f"UPDATE users SET {query_str} WHERE id = %s RETURNING id, first_name, last_name, email"
    values = list(updating_user.values())
    values.append(user_id)
    cursor.execute(query, values)
    conn.commit()

    updated_user = cursor.fetchone()

    cursor.close()
    release_connection(conn)

    return {"message": "User updated", "user": updated_user}


@router.get('')
async def get_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name, email FROM users")
    users = cursor.fetchall()

    cursor.close()
    release_connection(conn)
    return users


@router.get('/{user_id}')
async def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, first_name, last_name, email FROM users WHERE id = %s", (user_id, ))
    user = cursor.fetchone()

    cursor.close()
    release_connection(conn)

    return user


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        release_connection(conn)
        raise HTTPException(
            status_code=404, detail=f"User not found {user_id}")

    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()

    cursor.close()
    release_connection(conn)

    return {'message': f"User deleted {user_id}", "user": user}
