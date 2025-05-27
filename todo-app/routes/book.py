from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.db_connection import get_connection, release_connection
from helper.helper import dict_to_sql_query_string

router = APIRouter(prefix='/books', tags=['books'])


class Book(BaseModel):
    title: str
    description: str = None
    asin: int = None


class BookUpdate(BaseModel):
    title: str = None
    description: str = None
    asin: int = None


@router.post('')
async def add_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, description, asin) VALUES(%s, %s, %s) RETURNING id, title, description, asin", (book.title, book.description, book.asin))
    conn.commit()
    new_book = cursor.fetchone()

    cursor.close()
    release_connection(conn)

    return new_book


@router.get('')
async def get_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    cursor.close()
    release_connection(conn)

    return books


@router.put('/{book_id}')
async def update_book(book_id: int, book: BookUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    existing_book = cursor.fetchone()

    if not existing_book:
        cursor.close()
        release_connection(conn)
        raise HTTPException(
            status_code=404, detail=f"Book not found {book_id}")

    updating_book = book.dict(exclude_unset=True)
    query_str = ", ".join([f"{field} = %s" for field in updating_book.keys()])

    query = f"UPDATE books SET {query_str} WHERE id = %s RETURNING *"
    values = list(updating_book.values())
    values.append(book_id)
    cursor.execute(query, values)
    conn.commit()

    updated_book = cursor.fetchone()

    cursor.close()
    release_connection(conn)

    return updated_book


@router.get('/{book_id}')
async def get_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()

    cursor.close()
    release_connection(conn)

    return book


@router.delete('/{book_id}')
async def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    existing_book = cursor.fetchone()

    if not existing_book:
        cursor.close()
        release_connection(conn)
        raise HTTPException(
            status_code=404, detail=f"Book not found {book_id}")

    cursor.execute("DELETE FROM books WHERE id = %s RETURNING *", (book_id, ))
    deleted_book = cursor.fetchone()
    conn.commit()

    cursor.close()
    release_connection(conn)

    return deleted_book
