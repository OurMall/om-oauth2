from fastapi import APIRouter

from .authorize import authorize
from .known import known
from .client import client
from .token import token
from .auth import login

router = APIRouter(
    prefix="/oauth2"
)

"""
    :endpoints: OAuth2 main endpoints.
"""
router.include_router(
    router=authorize.router,
    tags=["Authorization"]
)

router.include_router(
    router=known.router,
    tags=["Know Authorization"]
)

router.include_router(
    router=login.router,
    tags=["User Log In"]
)

router.include_router(
    router=client.router,
    tags=["Dynamic Client Registration"]
)

router.include_router(
    router=token.router,
    tags=["Token Endpoints"]
)