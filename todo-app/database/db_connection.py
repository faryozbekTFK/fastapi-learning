import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(
    host='localhost',
    database='good_reads',
    user='postgres',
    password=1,
    minconn=1,
    maxconn=10,
    cursor_factory=RealDictCursor
)


def get_connection():
    return db_pool.getconn()


def release_connection(conn):
    if conn:
        db_pool.putconn(conn)
