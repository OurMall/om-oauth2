import datetime
from pydantic import Field
from beanie import Document, Insert, Replace, Indexed, after_event, before_event

from app.services.oauth_service import OAuth2Service

class Client(Document):
    application_id: Indexed(str, unique=True)
    application_secret: str | None
    redirect_uris: list[str]
    response_types: list[str] = Field(["code", "code id_token"])
    grant_types: list[str] = Field(["authorization_code"])
    application_type: str
    contact: str
    application_name: str
    logo_uri: str
    application_uri: str
    policy_uri: str
    tos_uri: str
    jwks_uri: str | None = Field(None)
    subject_type: str
    default_max_age: int | datetime.time = Field(datetime.timedelta(days=1).total_seconds())
    is_known: bool = Field(False)
    is_disabled: bool = Field(False)
    updated_at: int | datetime.datetime = Field(datetime.datetime.now())
    created_at: int | datetime.datetime | None
    
    @before_event(Insert)
    def set_app_credentials(self):
        self.application_id = next(OAuth2Service.generate_client_id())
        self.application_secret = next(OAuth2Service.generate_client_secret(length=25))
        self.created_at = datetime.datetime.now()
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "clients"
    
    class Settings:
        validate_on_save = True
    
    class Config:
        json_encoders = {
            id: lambda v: v.__str__()
        }