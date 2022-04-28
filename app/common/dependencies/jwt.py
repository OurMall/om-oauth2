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
    if isinstance(token, (str, bytes)):
        token: str | bytes = authorization.split(' ')[1] # ['Bearer', 'jwt'] = 'jwt'
        if not token:
            raise HTTPException(
                status_code=401,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Not valid authorization header"
                    }
                }
            )
        payload: dict[str, object] = jwt_provider.decode(
            encoded=token,
            validate=True
        )
        return payload
    pass

def verify(validate_account: bool = False):
    def _verify(
        authorization: str = Header(...),
        jwt_provider: JSONWebTokenService = Depends(get_jwt_provider())
    ):
        token: str | bytes = authorization.split(' ')[1]
        if isinstance(token, (str, bytes)):
            payload: dict[str, object] = jwt_provider.decode(
                encoded=token,
                validate=True
            )
        else:
            pass
    return verify

def is_known_client(
    payload: dict[str, object] = Depends(decode_authorization_header),
    jwt_provider: JSONWebTokenService = Depends(get_jwt_provider())
) -> bool | None:
    if payload.get("is_known") and payload.get("scopes"):
        is_known, scopes = payload.get("is_known"), payload.get("scopes")
        print(payload["is_known"])
        if isinstance(is_known, bool) and is_known:
            return is_known
        pass
    return False