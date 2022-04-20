from fastapi import APIRouter

router = APIRouter(
    prefix="/token",
    tags=["Token"]
)

@router.post("/")
async def refresh():
    pass

@router.post("/revoke")
async def revoke():
    pass