from fastapi import FastAPI 
from server.routers.auth_router import auth_router
from server.routers.user_router import user_router
from server.routers.driver_router import driver_router
from server.routers.trip_router import trip_router

app = FastAPI()

app.include_router(auth_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(driver_router, prefix='/api')
app.include_router(trip_router, prefix='/api')
