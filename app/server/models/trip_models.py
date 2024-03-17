from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class Driver(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    licenseNumber: str
    averageRating: float
    availability: bool
    createdAt: datetime
    updatedAt: datetime


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


class Trip(BaseModel):
    id: int
    origin: str
    destination: str
    startDateTime: Optional[datetime]
    endDateTime: Optional[datetime]
    distance: float
    fare: float
    duration: Optional[int]
    status: str
    createdAt: datetime
    updatedAt: datetime
    driver: Driver
    user: User


class TripsResponse(BaseModel):
    count: int
    trips: List[Trip]
