from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """SQLAlchemy基础模型"""
    __abstract__ = True

    # id = Column(Integer, primary_key=True, index=True)
    # created_at = Column(DateTime, default=datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # created_by = Column(String(50), nullable=True)
    # updated_by = Column(String(50), nullable=True)
