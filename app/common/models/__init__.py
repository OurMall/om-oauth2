from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    ...
    
    class Config:
        orm_mode=True
        arbitrary_types_allowed=True
        validate_assignment=True
