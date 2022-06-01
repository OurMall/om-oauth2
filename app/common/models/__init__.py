from pydantic import BaseModel as PydanticBaseModel
from pymongo.collection import ObjectId as BsonObjectId

class BaseModel(PydanticBaseModel):
    ...
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        #json_encoders = {ObjectId: str}

class PyObjectId(BsonObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError("ObjectId required")
        return str(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")