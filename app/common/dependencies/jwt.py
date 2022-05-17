from fastapi import HTTPException, Depends, Header
from app.services import JSONWebTokenService

def get_jwt_provider(**kwds: dict[str, object]):
    def _get_jwt_provider():
        return JSONWebTokenService(**kwds)
    return _get_jwt_provider

def decode_authorization_header(
    authorization: str = Header(...),
    jwt_provider: JSONWebTokenService = Depends(get_jwt_provider())
) -> dict[str, object]:
    access_token: str | bytes = authorization.split(' ')[1]
    if not access_token:
        #return None
        #TODO: delete if error.
        raise HTTPException(
            status_code=401,
            detail={
                "status": "fail",
                "response": {
                    "message": "No access token provided"
                }
            }
        )
    payload: dict[str, object] = jwt_provider.decode(
        encoded=access_token,
        validate=True
    )
    return payload

def decode_known_token(
    knownAuthorization: str = Header(..., title="Known Authorization", description="Known token in known authorization header"),
    jwt_provider: JSONWebTokenService = Depends(get_jwt_provider())
) -> dict[str, object]:
    known_token: str | bytes = knownAuthorization.split(' ')[1]
    if not known_token:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "fail",
                "response": {
                    "message": "No known authorization header provided"
                }
            }
        )
    payload: dict[str, object] = jwt_provider.decode(encoded=known_token, validate=True)
    return payload
