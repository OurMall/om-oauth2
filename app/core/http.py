import json
from beanie import PydanticObjectId
from pymongo.collection import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import *

class OJSONEncoder(json.JSONEncoder):
    
    def default(self, o: object) -> object:
        if isinstance(o, (ObjectId, PydanticObjectId)):
            return str(o)
        return json.JSONEncoder.default(self, o)

class HttpResponse:
    
    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def body(self) -> dict[str, object]:
        return self._body

    def __init__(self, *, status_code: int | str, body: dict[str, object]) -> None:
        super().__init__()
        if isinstance(status_code, (str)):
            status_code = int(status_code)
        self._status_code = status_code
        self._body = body
    
    def response(self) -> JSONResponse:
        compatible_body = jsonable_encoder(self.body)
        response = JSONResponse(
            content=compatible_body,
            status_code=self.status_code,
            media_type="application/json"
        )
        return response

