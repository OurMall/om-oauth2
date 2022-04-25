from pydantic import BaseModel

class BaseSchema(BaseModel):
    ...
    
    class Config:
        orm_mode=True
        arbitrary_types_allowed=True
        validate_assignment=True

class Address(BaseModel):
    formatted: str
    street_address: str
    locality: str
    region: str
    postal_code: str | None
    country: str

__all__ = ["Address"]