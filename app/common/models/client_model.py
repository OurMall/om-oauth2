import datetime
from pydantic import Field

from . import BaseModel

class ClientBase(BaseModel):
    client_id: str