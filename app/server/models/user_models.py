from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


# Model for an individual trip
class Trip(BaseModel):
    id: int
    origin: str
    destination: str
    startDateTime: Optional[datetime]
    endDateTime: Optional[datetime]
    distance: float
    fare: float
    duration: Optional[int]
    createdAt: datetime
    updatedAt: datetime


# Model for the user including a list of trips
class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    registrationDate: datetime
    averageRating: float
    location: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    trips: List[Trip]


# Model for the user including a list of trips
class UsersResponse(BaseModel):
    count: int
    users: List[User]
