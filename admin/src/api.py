from sqlalchemy.orm import Session

from . import models, schemas


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.Product):
    product = models.Product(
        title=product.title, image=product.image, likes=product.likes)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, product_data: schemas.Product):
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    product.title = product_data.title
    product.image = product_data.image
    product.likes = product_data.likes
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    db.delete(product)
    db.commit()


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id)


def create_user(db: Session, user: schemas.User):
    user = models.User(name=user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
