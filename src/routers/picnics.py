import datetime as dt
from fastapi import APIRouter, Query, HTTPException
from database import Session, Picnic, PicnicRegistration, City, User
from models import RegisterPicnicModel, PicnicModel, UserPicnicRegistration

picnics_router = APIRouter(prefix='/picnics')


@picnics_router.get('/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None,
                                              description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True,
                                   description='Включая уже прошедшие пикники'),
                offset: int = 0,
                limit: int = 20):
    """
    Список всех пикников
    """
    session = Session()
    picnics = session.query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    picnics = picnics.offset(offset).limit(limit)

    return [
        {
            'id': picnic.id,
            'city_id': picnic.city_id,
            'city_name': session.query(City).filter(
                City.id == picnic.city_id).first().name,
            'time': picnic.time,
            'users': [
                {
                    'id': pic.user.id,
                    'name': pic.user.name,
                    'surname': pic.user.surname,
                    'age': pic.user.age
                } for pic in session.query(PicnicRegistration).filter(PicnicRegistration.picnic_id == picnic.id).all()
            ]

        } for picnic in picnics
    ]


@picnics_router.post('/', summary='Picnic Add', tags=['picnic'])
def picnic_add(picnic: RegisterPicnicModel):
    session = Session()
    # Проверка существования города
    city = session.query(City).filter(City.id == picnic.city_id).first()
    if not city:
        raise HTTPException(status_code=400,
                            detail='Города с этим id не существует')

    # Проверка попытки регистрации в прошлом
    if picnic.datetime < dt.datetime.now():
        raise HTTPException(status_code=400,
                            detail='Машину времени еще не изобрели')

    picnic_object = Picnic(city_id=picnic.city_id, time=picnic.datetime)
    session.add(picnic_object)
    session.commit()
    return PicnicModel.from_orm(picnic_object)


@picnics_router.post('/usersignup/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(data: UserPicnicRegistration):
    session = Session()
    user = session.query(User).filter(User.id == data.user_id).first()

    # Проверка существования пользователя
    if not user:
        raise HTTPException(status_code=400,
                            detail='Пользователя с этим id не существует')
    picnic = session.query(Picnic).filter(Picnic.id == data.picnic_id).first()

    # Проверка существования пикника
    if not picnic:
        raise HTTPException(status_code=400,
                            detail='Пикника с этим id не существует')

    # Проверка повторной регистрации
    repeat = session.query(PicnicRegistration).filter(PicnicRegistration.picnic_id == picnic.id,
                                                      PicnicRegistration.user_id == user.id).first()
    if repeat:
        raise HTTPException(status_code=400,
                            detail='Пользователь уже зарегестрирован')

    registration = PicnicRegistration(user_id=user.id,
                                      picnic_id=picnic.id)
    session.add(registration)
    session.commit()

    return {'user': f'{user.name} {user.surname}',
            'picnic': picnic.id,
            'message': 'Визит на пикник зарегестрирован'}