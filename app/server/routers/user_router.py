from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from server.models.user_models import UsersResponse
from server.services.user_service import get_user, get_users

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


@user_router.get("/users", response_model=UsersResponse)
async def list_users(token: str = Depends(oauth2_scheme)):
    return await get_users(token)


@user_router.get("/users/{user_id}")
async def read_user(user_id: int, token: str = Depends(oauth2_scheme)):
    user_data = await get_user(user_id, token)
    return user_data
