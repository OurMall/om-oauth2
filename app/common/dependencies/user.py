from fastapi import Depends, HTTPException

from app.common import User

from .jwt import decode_authorization_header

def get_user(current: bool, fetch_links: bool=False, id: str | None=None, **kwds):
    async def _get_user(
        payload: dict[str, object] = Depends(decode_authorization_header)
    ) -> User:
        if current:
            user_id = payload.get("sub")
        else:
            user_id = id if id is not None else payload.get("sub")
        user = await User.get(user_id, fetch_links=fetch_links, ignore_cache=kwds.get("ignore_cache"))
        if not user:
            return None
        return user
    return _get_user
        
def verify_account(
    current_user: User = Depends(get_user(current=True))
) -> bool | HTTPException:
    if current_user.email_verified.__bool__():
        return True
    raise HTTPException(
        status_code=401,
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
    async def _has_permissions(
        user: User = Depends(get_user(current=True, fetch_links=True, ignore_cache=True))
    ):
        user_permissions = [str(permission.code_name) for permission in user.permissions]
        for permission in code_name:
            try:
                user_permissions.index(permission)
            except:
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
    async def _has_groups(
        user: User = Depends(get_user(current=True, fetch_links=True, ignore_cache=True))
    ):
        user_groups = [group.code_name for group in user.groups]
        for group in code_name:
            try:
                user_groups.index(group)
            except:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "fail",
                        "response": {
                            "message": "User not in the required group"
                        }
                    }
                )
        return True
    return _has_groups