from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.common import User, Group
from app.common.dependencies import security, jwt
from app.common.models.response_model import SuccessResponseModel

from .account import account

router = APIRouter(
    prefix="/user",
)

router.include_router(
    router=account.router,
    tags=["Account"]
)

@router.post("/group", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify)
])
async def add_user_groups(
    code_name: str = Body(..., title="Code Name", description="Code name for the group to add"),
    payload: dict[str, object] = Depends(jwt.decode_authorization_header)
):
    try:
        group = await Group.find_one(Group.code_name == code_name)
        user = await User.get(
            document_id=payload.get("sub"), 
            fetch_links=True,
            ignore_cache=True
        )
        user.groups.append(group)
        await user.save()
    except:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "An error was ocurred",
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
        