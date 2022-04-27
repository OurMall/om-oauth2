from fastapi import Depends, Header
from app.services import JSONWebTokenService

def get_jwt_provider(**kwds):
    def _get_jwt_provider():
        return JSONWebTokenService(**kwds)
    return _get_jwt_provider

def verify(validate_account: bool = False):
    def _verify(
        authorization: str = Header(...),
        jwt_provider: JSONWebTokenService = Depends(get_jwt_provider())
    ):
        token: str = authorization.split(' ')[1]
    return verify