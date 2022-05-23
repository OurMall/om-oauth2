import time
import datetime
from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse

from app.services import JSONWebTokenService
from app.common.dependencies import user, jwt, security
from app.common.models.token_model import TokenCredentials, TokenModel

router = APIRouter(
    prefix="/token",
    dependencies=[
        Depends(security.verify),
    ]
)

@router.post("/", response_model=TokenModel, status_code=201)
async def refresh(
    credentials: TokenCredentials,
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    jwt_provider.decode(
        encoded=credentials.refresh_token,
        validate=True
    )
    payload: dict[str, object] = jwt_provider.decode(
        encoded=credentials.access_token,
        validate=False
    )
    if payload["exp"] <= (time.time() + 1000):
        expiration = datetime.timedelta(days=1)
        access_token: str = jwt_provider.encode({
            "iss": payload.get("iss"),
            "sub": payload.get("sub"),
            "aud": payload.get("aud"),
            "azp": payload.get("azp"),
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + expiration,
            "scope": payload.get("scope")
        }, encrypt=True)
        refresh_token: str = jwt_provider.encode({
            "iss": payload.get("iss"),
            "azp": payload.get("azp"),
            "exp": datetime.datetime.utcnow() + (expiration * 2)
        }, encrypt=False)
        response = TokenModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=expiration.total_seconds()
        )
        return JSONResponse(
            content={
                "status": "success",
                "response": response.dict()
            },
            status_code=201,
            headers={
                "Authorization": f"Bearer {access_token}",
                "WWW-Authenticate": f"Bearer {access_token}"
            }
        )
    return JSONResponse(
        content={
            "status": "success",
            "response": {
                "access_token": credentials.access_token,
                "refresh_token": credentials.refresh_token
            }
        },
        status_code=200,
        headers={
            "Authorization": f"Bearer {credentials.access_token}",
            "WWW-Authenticate": f"Bearer {credentials.refresh_token}"
        }
    )

@router.post("/revoke")
async def revoke():
    pass