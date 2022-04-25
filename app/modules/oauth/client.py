from fastapi import APIRouter, Query

from app.common.models.client_model import ClientModel, ClientCreate

router = APIRouter(
    prefix="/connect",
)

@router.get("/register", response_model=None, status_code=200)
async def show_client(
    client_id: str = Query(..., title="Client ID", description="Client unique identifier into authorization server"),
):
    pass

@router.post("/register", response_model=None, status_code=201)
async def register_client(
    client: ClientCreate
):
    pass