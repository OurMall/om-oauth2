import datetime
from fastapi import APIRouter, BackgroundTasks, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.services import JSONWebTokenService, AuthService, email_client
from app.common import User, Profile, Group
from app.common.dependencies import jwt, security
from app.common.models.user_model import UserSignup
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/signup"
)

@router.post("/", response_model=SuccessResponseModel, status_code=201, summary="Signup", description="User registration")
async def signup(
    request: Request,
    user_credentials: UserSignup,
    background_tasks: BackgroundTasks,
    payload: dict[str, object] = Depends(jwt.decode_known_token),
    is_known: bool = Depends(security.is_known_client),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
    if is_known:
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
        try:
            new_user = User(
                given_name=user_credentials.given_name,
                family_name=user_credentials.family_name,
                middle_name=user_credentials.middle_name,
                gender=user_credentials.gender,
                email=user_credentials.email,
                password=AuthService.hash_password(user_credentials.password),
                phone_number=user_credentials.phone_number,
                profile=Profile(
                    picture=user_credentials.profile.picture
                ),
                birthdate=user_credentials.birthdate,
                zoneinfo=user_credentials.zoneinfo,
                locale=user_credentials.locale,
                groups=[group]
            )
            await User.insert_one(new_user)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Something went wrong"
                    }
                }
            )
        else:
            expiration = datetime.timedelta(days=1)
            access_token: str | bytes = jwt_provider.encode({
                "iss": str(request.base_url),
                "sub": new_user.id.__str__(), # Convert ObjectID to string.
                "aud": [
                    f"{str(request.base_url)}/connect/userinfo"
                ],
                "azp": payload["application_id"],
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + expiration,
                "scope": "openid all"
            }, encrypt=True)
            refresh_token: str | bytes = jwt_provider.encode({
                "iss": str(request.base_url),
                "azp": payload["application_id"],
                "exp": datetime.datetime.utcnow() + (expiration*2)
            }, encrypt=False)
            background_tasks.add_task(
                email_client.send_email,
                new_user.email,
                "Bienvenido a Our Mall",
                message="""
                    Hola, bienvenido a Our Mall
                    <br>
                    <a href="http://localhost:4200/profile/verifyAccount?token={0}">Verificar cuenta</a>
                """.format(access_token),
                format="html"
            )
            return JSONResponse(
                content={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": expiration.total_seconds(),
                    "token_type": "Bearer"
                },
                status_code=201,
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
                "message": "No known token provided"
            }
        }
    )