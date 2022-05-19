from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse

from app.services import JSONWebTokenService
from app.common.dependencies import user, jwt, security

router = APIRouter(
    prefix="/token",
    dependencies=[
        Depends(security.verify),
    ]
)

@router.post("/", response_model=None, status_code=201)
async def refresh(
    credentials: object,
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    pass

@router.post("/revoke")
async def revoke():
    pass