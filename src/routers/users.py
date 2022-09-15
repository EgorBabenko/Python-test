from fastapi import APIRouter, Query

from models import RegisterUserRequest, UserModel
from database import Session, User
from pydantic.class_validators import List

users_router = APIRouter(prefix='/users')


@users_router.get('/', summary='Список пользователей', tags=['users'], response_model=List[UserModel])
def users_list(min_age: int = Query(description='Минимальный возраст',
                                    default=None),
               max_age: int = Query(description='Максимальный возраст',
                                    default=None),
               offset: int = Query(description='Пропуск в выдаче', default=0),
               limit: int = Query(description='Лимит выдачи', default=20)):
    """
    Список пользователей
    """
    session = Session()
    min_age = min_age if min_age else 0
    if max_age:
        users = session.query(User).filter(User.age <= max_age,
                                           User.age >= min_age)
    else:
        users = session.query(User).filter(User.age >= min_age)

    users = users.offset(offset).limit(limit).all()
    return [UserModel.from_orm(user) for user in users]


@users_router.post('/', summary='Создание пользователя', response_model=UserModel, tags=['users'])
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)
