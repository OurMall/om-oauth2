import datetime
from beanie import PydanticObjectId
from beanie.operators import Set
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Depends, Body, Path
from fastapi.responses import JSONResponse

from app.core import HttpResponse
from app.common import User
from app.services import JSONWebTokenService, email_client
from app.common.dependencies import jwt, user
from app.common.models.user_model import UserModel, UserPartialUpdate
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/account",
    dependencies=[
        Depends(user.has_groups("client"))
    ]
)

@router.get("/", response_model=None, status_code=200)
async def account(
    payload: dict[str, object] = Depends(jwt.decode_authorization_header)
):
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

@router.patch("/{id}", response_model=SuccessResponseModel, status_code=201)
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

@router.post("/sendVerification", response_model=SuccessResponseModel, status_code=201)
async def send_account_verification(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Body(...),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
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
                <a href="http://localhost:4200/profile/verifyAccount?token={0}">Verificar cuenta</a>
            """.format(token),
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
        )

@router.post("/verify", response_model=SuccessResponseModel, status_code=201)
async def verify_account(
    token: str = Body(..., title="Token", description="Token for account validation"),
    payload: dict[str, object] = Depends(jwt.decode_authorization_header),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
    jwt_provider.decode(
        encoded=token,
        validate=True
    )
    user = await User.get(payload.get("sub"), fetch_links=True)
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
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "message": "user was verified"
                }
            },
            status_code=201
        )