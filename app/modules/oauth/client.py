from fastapi import APIRouter

router = APIRouter(
    prefix="/connect",
    tags=["Connect", "Clients"]
)

@router.post("/register", status_code=201)
async def register_client():
    pass