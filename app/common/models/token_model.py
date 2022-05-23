from pydantic import Field

from . import BaseModel

class TokenCredentials(BaseModel):
    access_token: str = Field(..., title="Access Token", description="Initial token provided by the server")
    refresh_token: str = Field(..., title="Refresh Token", description="Token for refresh the access token")
    token_type: str | None = Field(None, title="Type", description="Token type emited")

class TokenModel(TokenCredentials):
    expires_in: int