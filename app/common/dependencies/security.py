from fastapi import Depends, HTTPException

from .jwt import decode_known_token, decode_authorization_header

def is_known_client(
    payload: dict[str, object] = Depends(decode_known_token),
) -> bool | None:
    if payload.get("is_known"):
        is_known: bool = payload.get("is_known")
        if isinstance(is_known, bool) and is_known:
            return is_known
        pass
    raise HTTPException(
        status_code=401,
        detail={
            "status": "fail",
            "response": {
                "message": "No known client"
            }
        }
    )

def verify(
    payload: dict[str, object] | None = Depends(decode_authorization_header)
):
    if not payload:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "fail",
                "response": {
                    "message": "Missing bearer access token"
                }
            }
        )
    pass