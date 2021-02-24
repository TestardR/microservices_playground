from sqlalchemy.orm import Session

from . import models


def get_products(db: Session):
    return db.query(models.Product).all()
