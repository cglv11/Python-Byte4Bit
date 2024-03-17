from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from server.models.token_models import Token
from server.services.auth_service import authenticate_admin
from passlib.context import CryptContext

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    admin, token = await authenticate_admin(form_data.username, form_data.password)
    if not admin or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}
