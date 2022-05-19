from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.common import User, Group
from app.common.dependencies import security, user, jwt
from app.common.models.user_model import UserPartialUpdate

from .account import account

router = APIRouter(
    prefix="/user",
    dependencies=[
        Depends(security.verify),
    ]
)

router.include_router(
    router=account.router,
    tags=["Account"]
)

@router.patch("/{id}", response_model=None, status_code=201)
async def edit_user(
    id: str,
    user: UserPartialUpdate
):
    existented_user: User = await User.find_one(User.id == id)
    if not existented_user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "Not found user"
                }
            }
        )
    edited_user: User = await existented_user.set(user.dict(
        exclude_unset=True
    ))
    pass

@router.post("/group", response_model=None, status_code=201)
async def add_user_groups(
    code_name: str = Body(..., title="Code Name", description="Code name for the group to add"),
    payload: dict[str, object] = Depends(jwt.decode_authorization_header)
):
    user = await User.get(payload.get("sub"), fetch_links=True)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "Not found user"
                }
            }
        )
    try:
        group = await Group.find_one(Group.code_name == code_name)
        user.groups.append(group)
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
                    "message": "Se ha añadido el grupo al usuario"
                }
            },
            status_code=201
        )
        