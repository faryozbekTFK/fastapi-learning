from sqlalchemy import Column, Integer, String
from .config import Base

# https://www.youtube.com/watch?v=gBtwxKyFNdc&list=TLPQMTcwNDIwMjXLNNsX4nmw0Q&index=3


class Todo(Base):
    __tablename__ = 'todos'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, index=True)
    description: str = Column(String, index=True)
