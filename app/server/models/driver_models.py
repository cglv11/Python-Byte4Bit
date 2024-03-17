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


# Model for a driver including a list of trips
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
    trips: List[Trip]


# Model for the response that includes a list of drivers
class DriversResponse(BaseModel):
    count: int
    drivers: List[Driver]
