from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from server.models.trip_models import TripsResponse
from server.services.trip_service import get_trip, get_trips

trip_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


@trip_router.get("/trips", response_model=TripsResponse)
async def list_trips(token: str = Depends(oauth2_scheme)):
    return await get_trips(token)


@trip_router.get("/trips/{trip_id}")
async def read_trip(trip_id: int, token: str = Depends(oauth2_scheme)):
    trip_data = await get_trip(trip_id, token)
    return trip_data
