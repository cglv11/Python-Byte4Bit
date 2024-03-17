from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers.auth_router import auth_router
from server.routers.user_router import user_router
from server.routers.driver_router import driver_router
from server.routers.trip_router import trip_router
from decouple import config

is_production = config("PROJECT_ENVIRONMENT", default="DEVELOPMENT")

if is_production == "RELEASE":
    app = FastAPI(
        docs_url=None,  # Disable docs (Swagger UI)
        redoc_url=None,  # Disable redoc
    )
else:
    app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow the frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(driver_router, prefix="/api")
app.include_router(trip_router, prefix="/api")
