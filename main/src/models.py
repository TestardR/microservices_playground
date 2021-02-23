from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    image = Column(String(200))
    likes = Column(Integer, default=0)


class ProductUser(Base):
    __tablename__ = "product_user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')
