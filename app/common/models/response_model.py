from pydantic import Field

from . import BaseModel

class ResponseModel(BaseModel):
    status_code: int = Field(..., title="Status Code", description="HTTP status code for response")

class SuccessResponseModel(BaseModel):
    status: str = Field(..., title="Status", description="Text descriptional status")
    response: dict[str, object] = Field(..., title="Response", description="Body response to the client")