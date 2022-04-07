import datetime
from authlib.jose import jwt, errors
from authlib.common.encoding import to_bytes

class JSONWebToken:
    
    def __init__(self, **kwds: dict[str, object]) -> None:
        if kwds.get('headers'):
            self._headers = kwds['headers']
        self._headers = {
            'alg': 'RS256'
        }
    
    def encode(
        self,
        payload: dict[str, object],
        encrypt: bool|None
    ) -> str | bytes:
        if encrypt:
            self._headers = {
                'alg': 'RSA-OAEP-256',
                'enc': 'A256GCM'
            }
        try:
            encoded: bytes = jwt.encode(
                header=self._headers,
                payload=payload,
                key="my-key",
                check=True
            )
            token = str(encoded)
        except Exception as e:
            raise ValueError('Cannot encode the payload')
        else:
            return token
    
    def decode(
        self,
        encoded: str|bytes,
        validate: bool|None
    ) -> object:
        if not isinstance(encoded, bytes):
            encoded = to_bytes(encoded)
        dot_count: int = encoded.count(b'.')
        if dot_count == 2:
            pass
        try:
            payload: dict[str, object] = jwt.decode(
                s=encoded,
                key="my-key"
            )
            if validate:
                payload.validate(
                    leeway=datetime.timedelta(minutes=11).total_seconds()
                )
        except errors.ExpiredTokenError:
            return dict(
                message="Token expired"
            )
        except errors.BadSignatureError:
            return dict(
                message="Invalid token signature"
            )
        except errors.DecodeError:
            return dict(
                message="Failed to decode token"
            )
        else:
            return payload