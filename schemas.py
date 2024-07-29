import pydantic as pydantic
import datetime as datetime


class UserBase(pydantic.BaseModel):
    email: str
    name: str
    phone: str


class UserRequest(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True