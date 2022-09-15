import datetime as dt
from fastapi import APIRouter, Query
from database import Session, Picnic, PicnicRegistration, City

picnics_router = APIRouter(prefix='/picnics')


@picnics_router.get('/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None,
                                              description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True,
                                   description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(
                PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@picnics_router.post('/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = None, datetime: dt.datetime = None):
    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': Session().query(City).filter(City.id == p.id).first().name,
        'time': p.time,
    }


@picnics_router.post('/usersignup/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(*_, **__, ):
    """
    Регистрация пользователя на пикник
    (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
    """
    return ...
