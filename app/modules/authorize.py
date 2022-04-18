from fastapi import APIRouter, Response, Query

router = APIRouter(
    prefix="/authorize",
    tags=["Authorize"]
)

@router.get("/", summary="Authorize", description="Endpoint for user agent authorization")
async def authorize(
    response_type: str = Query(...),
    client_id: str = Query(...),
    redirect_uri: str = Query(...),
    scope: str = Query(...),
    state: str = Query(...),
    none: str = Query(...)
) -> Response:
    ...

@router.post("/")
async def authorize_callback():
    pass