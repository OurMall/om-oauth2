import enum
from pydantic import BaseModel, Field

class Gender(enum.Enum):
    MALE="male"
    FEMALE="female"
    OTHER="other"

class Currency(enum.Enum):
    USD='USD'
    COP='COP'

class ProductStatus(enum.Enum):
    NEW='new'
    USED='used'
    REFURBISHED='refurbished'

class BaseSchema(BaseModel):
    ...
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True

class Address(BaseSchema): # Change to BaseModel if error
    formatted: str | None = Field(None, title="Formatted", description="Complete address formatted")
    street_address: str | None = Field(None, title="Street", description="Street address")
    locality: str | None = Field(None, title="Locality", description="Address locality")
    region: str | None = Field(None, title="Region", description="Address region")
    postal_code: str | None = Field(None, title="Postal Code", description="Address postal code")
    country: str | None = Field(None, title="Country", description="Address country")

class SocialMedia(BaseSchema):
    name: str | None
    url: str | None
    logo_uri: str | None

class Price(BaseSchema):
    value: float | int = Field(..., title="Value", description="Price value")
    currency: Currency = Field(..., title="Currency", description="Price currency")