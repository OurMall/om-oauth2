import datetime
from pydantic import Field

from . import BaseModel

class ClientProfile(BaseModel):
    # TODO:// for general information about the client
    pass

class Client(BaseModel):
    id: str = Field(default=None)
    redirect_uris: list[str] = Field(default=None)
    secret: str|None = Field(default=None)
    profile: ClientProfile = Field(default=None)
    state: str = Field(default=None)
    created_at: datetime.datetime = Field(default=datetime.datetime.utcnow())