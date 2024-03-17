from pydantic import BaseModel


class Admin(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
