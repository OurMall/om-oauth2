from fastapi import HTTPException, APIRouter, Request, Query
from fastapi.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter(
    prefix="/known"
)

@router.get("/", response_class=HTMLResponse, status_code=200, summary="Known Client", description="Endpoint for authorize a known client")
async def authorize_known(
    request: Request,
    token: str = Query(..., title="Client Token", description="Token issued by the authorization server for the client")
):
    if not token or not isinstance(token, str):
        raise HTTPException(
            status_code=401,
            detail={
                "status": "fail",
                "response": {
                    "error": "Failed to authorize known client"
                }
            },
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
    print(request.base_url)
    print("Client Key", token)
    return templates.TemplateResponse(
        name="modules/login_client.html",
        context={
            "request": request
        },
        status_code=200
    )

@router.post("/", response_model=None, status_code=201)
async def authorize_known_client(
    request: Request,
):
    pass
