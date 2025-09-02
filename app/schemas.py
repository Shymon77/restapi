from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    extra: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True
