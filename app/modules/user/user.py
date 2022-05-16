from fastapi import APIRouter, Body, Depends, Query, HTTPException
from fastapi.responses import JSONResponse

from app.common import User, Group
from app.common.models.user_model import UserPartialUpdate
from app.common.dependencies import security, user

router = APIRouter(
    prefix="/user",
    dependencies=[
        Depends(security.verify)
    ]
)

@router.get("/me", response_model=None, status_code=200)
async def me(
    current_user: User = Depends(user.get_user(current=True))
):
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "User not found"
                }
            }
        )
    return JSONResponse(
        content={
            "status": "success",
            "response": {
                "user": current_user
            }
        },
        status_code=200
    )

@router.get("/verifyAccount", response_model=None, status_code=200)
async def verify_account(
    token: str = Query(...),
):
    pass

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
    code_name: str = Body(...),
    user: User = Depends(user.get_user(current=True))
):
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
    exitented_group: Group = await Group.find_one(Group.code_name == code_name)
    user.groups.append(exitented_group)
    await user.save()
    return JSONResponse(
        content={
            "status": "success",
            "response": {
                "message": "Se ha añadido el grupo al usuario"
            }
        }
    )
        