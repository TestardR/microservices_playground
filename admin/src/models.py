from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    image = Column(String(200))
    likes = Column(Integer, default=0)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(55))
