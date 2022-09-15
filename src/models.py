from datetime import datetime as dt
from pydantic import BaseModel
from sqlalchemy.orm.collections import InstrumentedList


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True


class RegisterPicnicModel(BaseModel):
    city_id: int
    datetime: dt


class PicnicModel(BaseModel):
    id: int
    city_id: int
    time: dt
    users: InstrumentedList

    class Config:
        orm_mode = True


class UserPicnicRegistration(BaseModel):
    user_id: int
    picnic_id: int