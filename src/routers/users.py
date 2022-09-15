from fastapi import APIRouter

from models import RegisterUserRequest, UserModel
from database import Session, User

users_router = APIRouter(prefix='/users')


@users_router.get('/', summary='')
def users_list():
    """
    Список пользователей
    """
    users = Session().query(User).all()
    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@users_router.post('/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)
