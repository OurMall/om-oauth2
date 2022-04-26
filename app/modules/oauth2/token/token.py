from fastapi import APIRouter

router = APIRouter(
    prefix="/token"
)

@router.post("/")
async def refresh():
    pass

@router.post("/revoke")
async def revoke():
    pass