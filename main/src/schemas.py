from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    image: str
    likes: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
