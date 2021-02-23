from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
import uvicorn

from . import api, models, schemas
from .database import SessionLocal, engine
from .producer import publish

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/api/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/api/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    db_users = api.get_users(db)
    return db_users


@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = api.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return api.create_user(db=db, user=user)


@app.get("/api/products/", response_model=List[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    db_products = api.get_products(db)
    publish()
    return db_products


@app.post("/api/products/", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    return api.create_product(db=db, product=product)


@app.get("/api/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = api.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put('/api/products/{product_id}', response_model=schemas.Product)
def update_product(product_id: int, product_data: schemas.Product, db: Session = Depends(get_db)):
    db_product = api.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = api.update_product(db, product_id, product_data)
    return updated_product


@app.delete('/api/products/{product_id}', response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    api.delete_product(db, product_id)


if __name__ == "__main__":
    uvicorn.run(app)
