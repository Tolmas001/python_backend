from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class ContactRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    phone: str = Field(
        min_length=5,
        max_length=30
    )

    email: EmailStr

    comment: str = Field(
        min_length=5,
        max_length=3000
    )