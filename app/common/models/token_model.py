from pydantic import Field

from . import BaseModel

class Token(BaseModel):
    access_token: str = Field(default=None)
    refresh_token: str = Field(default=None)
    type: str = Field(default=None)
    scopes: str = Field(default=None)
    is_revoke: bool = Field(default=False)
    is_expired: bool = Field(default=False)