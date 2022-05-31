from pydantic import Field
from . import BaseModel

class Profile(BaseModel):
    picture: str