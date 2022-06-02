import datetime
from pydantic import Field
from beanie import Document, Indexed, after_event, Replace

class Permission(Document):
    code_name: Indexed(str, unique=True) = Field(..., title="Code Name", description="Permission code name")
    name: str = Field(..., title="Name", description="Permission name")
    description: str = Field(..., title="Description", description="Permissions description")
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="Permission creation date")
    updated_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Updated AT", description="Permission last updated")
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "permissions"