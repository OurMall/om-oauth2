from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse

from app.common import User
from app.services import JSONWebTokenService
from app.common.dependencies import jwt, user

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
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "user": current_user
                }
            },
            status_code=200
        )

@router.post("/verify", response_model=None, status_code=200)
async def verify(
    token: str = Body(..., title="Token", description="Token for account validation"),
    payload: dict[str, object] = Depends(jwt.decode_authorization_header),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
):
    jwt_provider.decode(
        encoded=token,
        validate=True
    )
    user = await User.get(payload.get("sub"), fetch_links=True)
    if user.email_verified:
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
            status_code=200
        )