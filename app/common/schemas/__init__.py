from pydantic import BaseModel

class BaseSchema(BaseModel):
    ...
    
    class Config:
        orm_mode=True
        arbitrary_types_allowed=True
        validate_assignment=True

class Address(BaseModel):
    formatted: str | None
    street_address: str | None
    locality: str | None
    region: str | None
    postal_code: str | None
    country: str | None

class SocialMedia(BaseModel):
    name: str | None
    url: str | None
    logo_uri: str | None
