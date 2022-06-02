import datetime
from pydantic import Field
from beanie import Document, Link, Indexed, after_event, Replace

from .permission_schema import Permission

class Group(Document):
    code_name: Indexed(str, unique=True) = Field(..., title="Code Name", description="Group code name")
    name: str = Field(..., title="Name", description="Group name")
    description: str = Field(..., title="Description", description="Group description")
    permissions: list[Link[Permission]] = Field([], title="Permissions", description="Group permissions")
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="Group creation date")
    updated_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Updated AT", description="Group last updated")
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "groups"