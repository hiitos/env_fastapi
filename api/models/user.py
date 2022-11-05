from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship

from api.db import Base

# ============================= DBを定義 ============================= 

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(1024))
    nickname = Column(String(1024))
    email = Column(String(1024))
    adress = Column(String(1024))
    phonenumber = Column(String(1024))
    created_at = Column(Timestamp, server_default=current_timestamp())
    updated_at = Column(Timestamp, server_default=current_timestamp())

    user = relationship("Log", back_populates="log")

class Log(Base):
    __tablename__ = "logs"

    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    content = Column(String(1024))
    content_int = Column(Integer)
    created_at = Column(Timestamp, server_default=current_timestamp())

    log = relationship("User", back_populates="user")