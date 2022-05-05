import datetime
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.services import AuthService
from app.common import User, Profile, Group
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
    group = await Group.find_one(Group.code_name == "client")
    new_user = User(
        given_name=user_credentials.given_name,
        family_name=user_credentials.family_name,
        middle_name=user_credentials.middle_name,
        gender=user_credentials.gender,
        email=user_credentials.email,
        password=AuthService.hash_password(user_credentials.password),
        phone_number=user_credentials.phone_number,
        birthdate=user_credentials.birthdate,
        zoneinfo=user_credentials.zoneinfo,
        locale=user_credentials.locale,
        groups=[group]
    )
    await User.insert_one(new_user)
    if new_user:
        expiration = datetime.timedelta(days=1)
        access_token: str | bytes = jwt_provider.encode({
            "iss": str(request.base_url),
            "sub": new_user.email,
            "aud": [
                f"{str(request.base_url)}/connect/userinfo"
            ],
            #"azp": payload["application_id"],
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + expiration,
            "scope": "openid all"
        }, encrypt=True)
        refresh_token: str | bytes = jwt_provider.encode({
            "iss": str(request.base_url),
            #"azp": payload["application_id"],
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
        status_code=400,
        detail={
            "status": "fail",
            "response": {
                "message": "Can't create the user"
            }
        }
    )