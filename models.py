from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    


class Record(Base):
    __tablename__ = "record"



class Friend(Base):
    __tablename__ = "friend"