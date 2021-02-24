from typing import List

from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
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


@app.get("/api/products/", response_model=List[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    db_products = api.get_products(db)
    return db_products

