from pydantic import Field
from . import BaseModel

class Profile(BaseModel):
    genre: object = Field(None)
    phone_number: str = Field(None)
    photo: str|bytes = Field(None)
    biography: str = Field(None)
    location: str = Field(None)
    address: str = Field(None)
    postal_code: str|int = Field(None)