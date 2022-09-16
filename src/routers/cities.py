from fastapi import APIRouter, Body, HTTPException, Query, Response
from pydantic.class_validators import List

from database import City, Session
from external_requests import CheckCityExisting
from models import CityModel, CityModelOutput

cities_router = APIRouter(prefix='/cities')


@cities_router.post('/', summary='Добавление города',
                    description='Создание города по его названию',
                    tags=['cities'],
                    response_model=CityModelOutput)
def create_city(city: CityModel):
    if city is None:
        raise HTTPException(status_code=400,
                            detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(city.name):
        raise HTTPException(status_code=400,
                            detail='Такой город не существует')

    # Проверка повторного создания города
    city_object = Session().query(City).filter(
        City.name == city.name.capitalize()).first()

    if city_object:
        raise HTTPException(status_code=400,
                            detail='Такой город уже в базе')
    else:
        city_object = City(name=city.name.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id,
            'name': city_object.name,
            'weather': city_object.weather}


@cities_router.get('/', summary='Список городов',
                   tags=['cities'],
                   response_model=List[CityModelOutput])
def cities_list(q: str = Query(description="Поиск города по названию",
                               default=None),
                offset: int = Query(description='Пропуск городов в выдаче',
                                    default=0),
                limit: int = Query(description='Лимит выдачи', default=20)):
    """
    Получение списка городов
    """
    session = Session()
    # реализация поиска по частичному/полному вхождению
    if q:
        cities = session.query(City).filter(
            City.name.contains(q)).offset(offset).limit(limit).all()
    else:
        cities = session.query(City).offset(offset).limit(limit).all()

    return [{'id': city.id,
             'name': city.name,
             'weather': city.weather} for city in cities]

