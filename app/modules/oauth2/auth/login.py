import datetime
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import Response, JSONResponse
from passlib.context import CryptContext

from app.services import JSONWebTokenService, AuthService
from app.common import User
from app.common.dependencies import jwt
from app.common.models.user_model import UserLogin

router = APIRouter(
    prefix="/login"
)

@router.post("/", response_model=None, status_code=200)
async def login(
    request: Request,
    user_credentials: UserLogin,
    payload: dict[str, object] = Depends(jwt.decode_authorization_header),
    is_known: bool = Depends(jwt.is_known_client),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    user = await User.find_one(User.email == user_credentials.email)
    if is_known:
        if not user:
            raise HTTPException(
                status_code=401,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Invalid user credentials"
                    }
                }
            )
        if AuthService.verify_password(user_credentials.password, user.password):
            expiration = datetime.timedelta(days=1)
            access_token: str | bytes = jwt_provider.encode({
                "iss": str(request.base_url),
                "sub": user.email,
                "aud": [
                    f"{str(request.base_url)}/connect/userinfo"
                ],
                "azp": payload["application_id"],
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + expiration,
                "scope": "openid all"
            }, encrypt=True)
            refresh_token: str | bytes = jwt_provider.encode({ # Is issued for refresh the access token
                "iss": str(request.base_url),
                "azp": payload["application_id"],
                "exp": datetime.datetime.utcnow() + (expiration*2)
            }, encrypt=False)
            return JSONResponse(
                content={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": expiration.total_seconds(),
                    "token_type": "Bearer"
                },
                status_code=200,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "WWW-Authenticate": f"Bearer {access_token}"
                }
            )
        raise HTTPException(
            status_code=401,
            detail={
                "status": "fail",
                "response": {
                    "message": "Invalid user credentials"
                }
            }
        )
    raise HTTPException(
        status_code=403,
        detail={
            "status": "fail",
            "response": {
                "message": "No known token provided"
            }
        }
    )