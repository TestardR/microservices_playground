from fastapi import FastAPI, Depends, status, Response
import requests
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, JSONResponse
from typing import List
import uvicorn

from . import api, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.post("/api/products/{product_id}/like", response_model=schemas.User)
def like_product(product_id: int, response: Response, db: Session = Depends(get_db)):
    req = requests.get('http://host.docker.internal:5000/api/users/random')
    json = req.json()
    try:
        productUser = models.ProductUser(
            user_id=json['id'], product_id=product_id)
        db.add(productUser)
        db.commit()
        db.refresh(productUser)
    except:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

    return JSONResponse({'message': 'success'})
