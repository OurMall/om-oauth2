import time
from reactivex import Observable, of,  operators as op
from fastapi import Depends, Request, HTTPException

from .jwt import decode_known_token, decode_authorization_header, get_jwt_provider

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

def limit_request():
    async def _limit_request():
        increment = __increment_request_counter__()
        print(next(increment))
        """counter: Observable = of(5)
        counter.pipe(
            op.reduce(lambda acc, x: acc + x, 10)
        )
        counter.subscribe(
            on_next = lambda value: print(value)
        )"""
        pass
    return _limit_request

def __increment_request_counter__() -> int:
    counter = 1
    while True:
        yield counter
        counter += 1
        print("generator", counter)