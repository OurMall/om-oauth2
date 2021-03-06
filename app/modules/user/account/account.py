import datetime
from beanie import PydanticObjectId, WriteRules
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Response, Depends, Body, Path

from app.core import HttpResponse, settings
from app.common import User
from app.services import JSONWebTokenService, AuthService, email_client
from app.common.dependencies import jwt, security, user
from app.common.models.user_model import UserModel, UserPartialUpdate, UserResetPassword
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/account"
)

@router.get("/", response_model=SuccessResponseModel, status_code=200, dependencies=[
    Depends(security.verify)
])
async def account(
    payload: dict[str, object] = Depends(jwt.decode_authorization_header)
) -> Response:
    try:
        current_user = await User.get(
            document_id=payload.get("sub"), 
            fetch_links=True, 
            ignore_cache=True
        )
    except:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "An error was ocurred"
                }
            }
        )
    else:
        user = UserModel(**current_user.dict())
        return HttpResponse(
            status_code=200, 
            body=user.dict(
                exclude={
                    "password"
                },
                exclude_none=True
            )
        ).response()

@router.get("/{id}", response_model=SuccessResponseModel, status_code=200)
async def specific_account(
    id: str = Path(..., title="ID", description="User to find unique identifier")
) -> Response:
    try:
        if isinstance(id, str):
            id = PydanticObjectId(id)
        user = await User.get(
            document_id=id,
            ignore_cache=True,
            fetch_links=True
        )
        if not user:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "User not found"
                    }
                }
            )
        user_response = UserModel(**user.dict())
    except:
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
        return HttpResponse(
            status_code=200,
            body=user_response.dict(
                exclude={
                    "password"
                },
                exclude_none=True
            )
        ).response()

@router.patch("/{id}", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify)
])
async def edit_account(
    changed_account: UserPartialUpdate,
    id: str = Path(..., title="Identifier", description="User unique identifier")
):
    if isinstance(id, (str)):
        id = PydanticObjectId(id)
    try:
        user: User = await User.find_one(
            User.id == id, 
            fetch_links=False, 
            ignore_cache=True
        )
        await user.set({ "profile": changed_account.profile.dict(
            exclude_unset=True,
            exclude_none=True
        )})
    except:
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
        
        return HttpResponse(
            status_code=201,
            body={
                "status": "success",
                "response": {
                    "message": "User account was edited"
                }
            }
        ).response()

@router.post("/sendVerification", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify),
    Depends(security.limit_request)
])
async def send_account_verification(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Body(...),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    try:
        user = await User.find_one(User.email == email)
        expiration = datetime.timedelta(minutes=60)
        token = jwt_provider.encode({
            "iss": str(request.base_url),
            "sub": user.id.__str__(),
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + expiration,
        }, encrypt=True)
        background_tasks.add_task(
            email_client.send_email,
            user.email,
            "Verificar cuenta",
            message="""
                Hola, bienvenido a Our Mall
                <br>
                <a href="{0}/profile/verifyAccount?token={1}">Verificar cuenta</a>
            """.format(settings.CLIENT_ENDPOINT, token),
            format="html"
        )
    except:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "Cant send email verification"
                }
            }
        )
    else:
        return HttpResponse(
            status_code=201,
            body={
                "status": "success",
                "response": {
                    "message": "Account verification sent"
                }
            }
        ).response()

@router.post("/verify", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify)
])
async def verify_account(
    token: str = Body(..., title="Token", description="Token for account validation"),
    payload: dict[str, object] = Depends(jwt.decode_authorization_header),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    jwt_provider.decode(
        encoded=token,
        validate=True
    )
    user = await User.get(
        document_id=payload.get("sub"), 
        fetch_links=True,
        ignore_cache=True
    )
    if user.email_verified.__bool__():
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "user is already verified"
                }
            }
        )
    try:
        user.email_verified = True
        await user.save()
    except:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "An error was ocurred"
                }
            }
        )
    else:
        return HttpResponse(
            status_code=201,
            body={
                "status": "success",
                "response": {
                    "message": "User was verified"
                }
            }
        ).response()

@router.post("/forgotPassword", response_model=SuccessResponseModel, status_code=201)
async def forgot_password(
    backgroundTasks: BackgroundTasks,
    email: str = Body(..., title="Email", description="User email for password reset"),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
    try:
        user = await User.find(
            User.email == email
        ).first_or_none()
        if not user:
            return HttpResponse(
                status_code=401,
                body={
                    "status": "fail",
                    "response": {
                        "message": "Not user found"
                    }
                }
            ).response()
        token: str = jwt_provider.encode({
            "sub": user.id.__str__(),
            "email": user.email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, encrypt=True)
        backgroundTasks.add_task(
            email_client.send_email,
            email,
            "Resetear contrase??a",
            message="""
                Parece que has perdido acceso a tu cuenta
                <a href="{0}/login/resetPassword?token={1}">Resetea tu contrase??a</a>
            """.format(settings.CLIENT_ENDPOINT, token),
            format="html"
        )
    except Exception as e:
        print(e)
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
        return HttpResponse(
            status_code=201,
            body={
                "status": "success",
                "response": {
                    "message": "Email sent"
                }
            }
        ).response()

@router.post("/resetPassword", response_model=SuccessResponseModel, status_code=201)
async def reset_password(
    password_credentials: UserResetPassword = Body(...),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
    try:
        payload: dict[str, object] = jwt_provider.decode(
            encoded=password_credentials.token,
            validate=True
        )
        user = await User.get(
            document_id=payload['sub']
        )
        if not password_credentials.new_password == password_credentials.confirm_password:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Not match passwords"
                    }
                }
            )
        new_password = AuthService.hash_password(password_credentials.new_password)
        #user.password = new_password
        await user.set({
            User.password: new_password
        })
    except:
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
        return HttpResponse(
            status_code=201,
            body={
                "status": "success",
                "response": {
                    "message": "Password reset"
                }
            }
        ).response()
    