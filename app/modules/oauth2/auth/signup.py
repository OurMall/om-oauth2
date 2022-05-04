import datetime
from fastapi import APIRouter, Request, HTTPException, Depends

from app.services import AuthService
from app.common import User
from app.common.dependencies import jwt
from app.common.models.user_model import UserSignup
from app.services.jwt_service import JSONWebTokenService

router = APIRouter(
    prefix="/signup"
)

@router.post("/", response_model=None, status_code=200)
async def signup(
    request: Request,
    user_credentials: UserSignup,
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
    existented_user = await User.find_one(User.email == user_credentials.email)
    if existented_user:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "User exists"
                }
            }
        )
    user_credentials.password = AuthService.hash_password(user_credentials.password)
    new_user = User(**user_credentials)
    await User.insert_one(new_user)
    if new_user:
        expiration = datetime.timedelta(days=1)
        access_token: str | bytes = jwt_provider.encode({
            "iss": str(request.base_url),
            "sub": new_user.id,
            "aud": [
                f"{str(request.base_url)}/connect/userinfo"
            ],
            #"azp": payload["application_id"],
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + expiration,
            "scope": "openid all"
        }, encrypt=True)
        refresh_token: str | bytes = jwt_provider.encode({ # Is issued for refresh the access token
            "iss": str(request.base_url),
            #"azp": payload["application_id"],
            "exp": datetime.datetime.utcnow() + (expiration*2)
        })
        pass
    raise HTTPException(
        status_code=400,
        detail={
            "status": "fail",
            "response": {
                "message": "Can't create the user"
            }
        }
    )