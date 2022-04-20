from fastapi import APIRouter

from app.common.models.client_model import ClientModel, ClientCreate

router = APIRouter(
    prefix="/connect",
    tags=["Connect", "Clients"]
)

@router.post("/register", response_model=ClientModel, status_code=201)
async def register_client(client: ClientCreate):
    pass