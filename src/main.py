from fastapi import FastAPI
from routers.cities import cities_router
from routers.users import users_router
from routers.picnics import picnics_router


app = FastAPI()

app.include_router(cities_router)
app.include_router(users_router)
app.include_router(picnics_router)

