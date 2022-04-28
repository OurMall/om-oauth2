from fastapi import APIRouter, Response, HTTPException, Depends
from passlib.context import CryptContext

from app.services import JSONWebTokenService
from app.common import User
from app.common.dependencies import jwt
from app.common.models.user_model import UserLogin

router = APIRouter(
    prefix="/login"
)

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/", response_model=None, status_code=200)
async def login(
    user_credentials: UserLogin,
    is_known: bool = Depends(jwt.is_known_client),
    jwt_provider: JSONWebTokenService = Depends(jwt.get_jwt_provider())
) -> Response:
    user = await User.find_one(User.email == user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "fail",
                "response": {
                    "message": "Invalid user credentials"
                }
            }
        )
    if verify_password(user_credentials.password, user.password):
        pass
    raise HTTPException(
        status_code=401,
        detail={
            "status": "fail",
            "response": {
                "message": "Invalid user credentials"
            }
        }
    )

def verify_password(plain: str, hash: str | bytes) -> bool:
    return password_context.verify(plain, hash)

def hash_password(plain: str) -> str | bytes:
    return password_context.hash(plain)