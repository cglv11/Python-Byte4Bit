from fastapi import FastAPI 
from routers.auth_router import auth_router
from routers.user_router import user_router
from routers.driver_router import driver_router

app = FastAPI()

app.include_router(auth_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(driver_router, prefix='/api')
