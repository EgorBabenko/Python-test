from fastapi import Query
from datetime import datetime as dt
from pydantic import BaseModel
from sqlalchemy.orm.collections import InstrumentedList
from pydantic.class_validators import List


class RegisterUserRequest(BaseModel):
    name: str = Query(..., description='Имя пользователя')
    surname: str = Query(..., description='Фамилия пользователя')
    age: int = Query(..., description='Возраст пользователя')


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True



class RegisterPicnicModel(BaseModel):
    city_id: int = Query(..., description='Id города')
    datetime: dt = Query(..., description='дата и время')


class PicnicModel(BaseModel):
    id: int
    city_id: int
    time: dt
    users: List[UserModel]

    class Config:
        orm_mode = True


class UserPicnicRegistration(BaseModel):
    user_id: int = Query(..., description='id пользователя')
    picnic_id: int = Query(..., description='id пикника')


class CityModel(BaseModel):
    name: str = Query(..., description='Название города')


class CityModelOutput(BaseModel):
    id: int
    name: str
    weather: float


class UserPicnicRegistrationOutput(BaseModel):
    user: str
    picnic: int
    message: str


class PicnicOutput(BaseModel):
    id: int
    city_id: int
    city_name: str
    time: dt
    users: List[UserModel]

