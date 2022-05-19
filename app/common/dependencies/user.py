from fastapi import Depends, HTTPException

from app.common import User

from .jwt import decode_authorization_header

def get_user(current: bool, id: str | None=None):
    async def _get_user(
        payload: dict[str, object] = Depends(decode_authorization_header)
    ) -> User:
        if current:
            user_id = payload.get("sub")
        else:
            user_id = id if id is not None else payload.get("sub")
        user = await User.get(user_id)
        if not user:
            return None
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

def has_permissions(code_name: list[str] | str):
    if(isinstance(code_name, str)):
        code_name = [code_name]
    async def _has_permissions(payload: dict[str, object] = Depends(decode_authorization_header)):
        user = await User.get(payload.get("sub"), fetch_links=True)
        for _ in code_name:#range(0, len(code_name)):
            user_permissions = [str(permission.code_name) for permission in user.permissions]
            if not user_permissions == code_name:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "fail",
                        "response": {
                            "message": "User doesn't have permissions"
                        }
                    }
                )
        return True
    return _has_permissions

def has_groups(code_name: list[str] | str):
    if(isinstance(code_name, str)):
        code_name = [code_name]
    async def _has_groups(payload: dict[str, object] = Depends(decode_authorization_header)):
        user = await User.get(payload.get("sub"), fetch_links=True)
        for _ in code_name: #range(0, len(code_name)):
            user_groups = [str(group.code_name) for group in user.groups]
            if not user_groups == code_name:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "fail",
                        "response": {
                            "message": "User not in the valid group"
                        }
                    }
                )
        return True
    return _has_groups