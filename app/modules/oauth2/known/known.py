import datetime
from fastapi import HTTPException, APIRouter, Request, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse, Response

from app.core import templates
from app.services import JSONWebTokenService
from app.common import Client
from app.common.dependencies import jwt
from app.common.models.client_model import ClientCredentials

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
    credentials: ClientCredentials,
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    client = await Client.find_one({"application_id": credentials.application_id, "application_secret": credentials.application_secret})
    if not client:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "Client didn't exist"
                }
            },
        )
    if not client.is_known:
        raise HTTPException(
            status_code=403,
            detail={
                "status": "fail",
                "response": {
                    "message": "No known application"
                }
            },
            headers={
                "WWW-Authenticate": "Bearer",
                "Authentication": "Bearer"
            }
        )
    # TODO:// Create JWT for Known Client authorization
    # TODO:// PASS the access known token to the login endpoint
    expiration = datetime.timedelta(minutes=60)
    known_token: str | bytes = jwt_provider.encode({
        "application_id": client.application_id,
        "is_known": client.is_known,
        "iss": str(request.url),
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + expiration,
        "scopes": "all"
    }, encrypt=True)
    return JSONResponse(
        content={
            "known_token": known_token,
            "expires_in": expiration.total_seconds(),
            "token_type": "Bearer"
        },
        status_code=201,
    )
    