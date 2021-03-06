import datetime
from pydantic import Field
from beanie import Document, Replace, Indexed, after_event

class Service(Document):
    code_name: Indexed(str, unique=True)
    name: Indexed(str)
    description: str
    activate: bool
    created_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Created AT", description="Service created date")
    updated_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Updated AT", description="Service last update")
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "services"
    
    class Settings:
        validate_on_save = True