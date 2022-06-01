from pydantic import BaseModel, Field

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

class SocialMedia(BaseSchema): # Change to BaseModel if error
    name: str | None
    url: str | None
    logo_uri: str | None
