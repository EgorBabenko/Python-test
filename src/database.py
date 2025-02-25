from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from external_requests import GetWeatherRequest

# Создание сессии
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       connect_args={'check_same_thread': False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Подключение базы (с автоматической генерацией моделей)
Base = declarative_base()


class City(Base):
    """
    Город
    """
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    @property
    def weather(self) -> str:
        """
        Возвращает текущую погоду в этом городе
        """
        r = GetWeatherRequest()
        weather = r.get_weather(self.name)
        return weather

    def __repr__(self):
        return f'<Город "{self.name}">'


class User(Base):
    """
    Пользователь
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<Пользователь {self.surname} {self.name}>'


class Picnic(Base):
    """
    Пикник
    """
    __tablename__ = 'picnic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    # Получение названия города, в котором проходит пикник
    @property
    def city_name(self):
        session = Session()
        return session.query(City).filter(City.id == self.city_id).first().name

    # Получение списка объектов пользователей - участников пикника
    @property
    def users(self):
        session = Session()

        users = [
            {
                'id': pic.user.id,
                'name': pic.user.name,
                'surname': pic.user.surname,
                'age': pic.user.age
            } for pic in session.query(PicnicRegistration).filter(
                PicnicRegistration.picnic_id == self.id).all()
        ]

        return users



    def __repr__(self):
        return f'<Пикник {self.id}>'


class PicnicRegistration(Base):
    """
    Регистрация пользователя на пикник
    """
    __tablename__ = 'picnic_registration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    picnic_id = Column(Integer, ForeignKey('picnic.id'), nullable=False)

    user = relationship('User', backref='picnics')
    picnic = relationship('Picnic', backref='guests')

    def __repr__(self):
        return f'<Регистрация {self.id}>'


Base.metadata.create_all(bind=engine)
