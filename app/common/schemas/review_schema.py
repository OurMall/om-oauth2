import datetime
from beanie import Document
from pydantic import Field

class Review(Document):
    user_id: str = Field(..., title="User ID", description="User that make the review")
    comment: str = Field(..., title="Comment", description="user comment", max_length=300)
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="Review creation date")
    
    class Collection:
        name = "reviews"
    
    class Settings:
        use_state_management = True
        validate_on_save = True