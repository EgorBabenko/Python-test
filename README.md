## Локальный старт
1. Клонируйте репозиторий:
```angular2html
git clone git@github.com:EgorBabenko/Python-test.git
```
2. В директории склонированного репозитория создайте и активируйте виртуальное окружение
```angular2html
python3 -m venv venv
source venv/bin/activate
```
3. Установите зависимости:
```angular2html
pip install -r requirements.txt
```
4. Запуск приложения:
```angular2html
cd src/
uvicorn main:app --reload
```

Документация API доступна по адресам:
 - http://127.0.0.1:8000/redoc
 - http://127.0.0.1:8000/doc

### TODO:
- Разнести функционал ендпойнтов в отдельные пакеты (cities, users, picnics), создать в каждом свой models.py. Иначе с ростом функционала код в соответствующих файлах станет слишком громоздким.
- Вынести функционал проверок, запросов к БД в отдельный пакет utils, разгрузив код api функций. В этот же пакет перенести код external_requests.py
