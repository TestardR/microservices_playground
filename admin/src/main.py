from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
import uvicorn

from . import api, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/products/", response_model=List[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    db_products = api.get_products(db)
    return db_products


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    return api.create_product(db=db, product=product)


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = api.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put('/products/{product_id}', response_model=schemas.Product)
def update_product(product_id: int, product_data: schemas.Product, db: Session = Depends(get_db)):
    db_product = api.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = api.update_product(db, product_id, product_data)
    return updated_product


@app.delete('/products/{product_id}', response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    api.delete_product(db, product_id)
