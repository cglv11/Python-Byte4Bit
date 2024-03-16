from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from models.driver_models import DriversResponse
from services.driver_service import get_driver, get_drivers
from services.user_service import get_user, get_users

driver_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

@driver_router.get("/drivers", response_model=DriversResponse)
async def list_drivers(token: str = Depends(oauth2_scheme)):
    return await get_drivers(token)

@driver_router.get("/drivers/{driver_id}")
async def read_driver(driver_id: int, token: str = Depends(oauth2_scheme)):
    driver_data = await get_driver(driver_id, token)
    return driver_data
