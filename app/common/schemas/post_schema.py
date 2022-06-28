import datetime
from beanie import Document, Replace, after_event
from pydantic import Field

class Post(Document):
    title: str = Field(..., title="Title", description="Post title")
    content: str = Field(..., title="Content", description="Post content", max_length=3000)
    image: str = Field(None, title="Image", description="Post image")
    is_public: bool = Field(True, title="Privacy", description="Post privacy")
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="Post creation date")
    updated_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Updated AT", description="Post updated date")
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "posts"
    
    class Settings:
        use_state_management = True
        validate_on_save = True