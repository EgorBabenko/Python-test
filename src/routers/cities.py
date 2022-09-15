from fastapi import APIRouter, HTTPException, Query
from external_requests import CheckCityExisting
from database import Session, City
from models import CityModel


cities_router = APIRouter(prefix='/cities')


@cities_router.post('/', summary='Create City',
                    description='Создание города по его названию')
def create_city(city: CityModel):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == city.name.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.name.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@cities_router.get('/', summary='Get Cities')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    cities = Session().query(City).all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]

