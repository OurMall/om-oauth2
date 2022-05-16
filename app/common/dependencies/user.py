from fastapi import Depends, HTTPException

from app.common import User

from .jwt import decode_authorization_header

def get_user(current: bool):
    async def _get_user(
        payload: dict[str, object] = Depends(decode_authorization_header)
    ) -> User:
        if current:
            user_id: str = payload.get("sub")
            user = await User.get(user_id, fetch_links=True)
            if not user:
                return None
            pass
        return user
    return _get_user
        
def verify_account(
    current_user: User = Depends(get_user(current=True))
) -> bool:
    if current_user.email_verified:
        return True
    raise HTTPException(
        status_code=403,
        detail={
            "status": "fail",
            "response": {
                "message": "User account unvalidated"
            }
        }
    )