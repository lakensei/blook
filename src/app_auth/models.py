from sqlalchemy import Column, String

from src.infrastructure.database.impl.sqlalchemy.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id = Column(String(50), primary_key=True, index=True)
    username = Column(String(50))
