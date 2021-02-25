from random import randint

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import models, schemas
from .producer import publish


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(
        title=product.title, image=product.image, likes=product.likes)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    publish('product_created', jsonable_encoder(db_product))
    return product


def update_product(db: Session, product_id: int, product_data: schemas.Product):
    db_product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    db_product.title = product_data.title
    db_product.image = product_data.image
    db_product.likes = product_data.likes
    db.commit()
    db.refresh(db_product)
    publish('product_updated', jsonable_encoder(db_product))
    return db_product


def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    db.delete(product)
    db.commit()
    publish('product_deleted', product_id)


def get_users(db: Session):
    return db.query(models.User).all()


def get_random_id():
    return {"id": randint(0, 100)}


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id)


def create_user(db: Session, user: schemas.User):
    user = models.User(name=user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
