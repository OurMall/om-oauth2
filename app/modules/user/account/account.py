from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse

from app.core import HttpResponse
from app.common import User
from app.services import JSONWebTokenService
from app.common.dependencies import jwt, user
from app.common.models.user_model import UserModel

router = APIRouter(
    prefix="/account",
    dependencies=[
        Depends(user.has_groups("client"))
    ]
)

EMAIL_RECOVERY_FORMAT = """
    <h2>
        hasdjLSDJAS
    </h2>
"""

@router.get("/", response_model=None, status_code=200)
async def account(
    payload: dict[str, object] = Depends(jwt.decode_authorization_header)
):
    try:
        current_user = await User.get(payload.get("sub"), fetch_links=True)
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
        """return HttpResponse(
            status_code=200, 
            body=current_user.dict()
        ).response()"""
        print(current_user.dict())
        return current_user.dict(
                exclude={
                    #"id",
                    "password",
                    "workspaces",
                    "permissions",
                    "groups"
                }
            )

@router.post("/verify", response_model=None, status_code=201)
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