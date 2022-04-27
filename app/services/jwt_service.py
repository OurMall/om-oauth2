import datetime
from pathlib import Path
from authlib.jose import jwt, errors
from authlib.common.encoding import to_bytes

from app.core import settings

class JSONWebTokenService:
    
    def __init__(self, **kwds: dict[str, object]) -> None:
        if kwds.get('headers'):
            self._headers = kwds['headers']
        self._headers = {
            'alg': 'RS256'
        }
    
    def encode(
        self,
        payload: dict[str, object],
        encrypt: bool | None
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
                key=self._load_key,
                check=True
            )
            token = str(encoded)
        except Exception as e:
            raise ValueError('Cannot encode the payload')
        else:
            return token
    
    def decode(
        self,
        encoded: str | bytes,
        validate: bool | None
    ) -> object:
        if not isinstance(encoded, bytes):
            encoded = to_bytes(encoded)
        #dot_count: int = encoded.count(b'.')
        try:
            payload: dict[str, object] = jwt.decode(
                s=encoded,
                key=self._load_key
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
    
    def revoke(self):
        pass
    
    def _load_key(
        self, 
        header: dict[str, object], 
        payload: dict[str, object], 
        private_key: bool=False
    ):
        match header['alg']:
            case 'RS256':
                if private_key:
                    key: bytes | str = self._get_rsa_key(private=True)
                else:
                    key = self._get_rsa_key()
                return key
            case 'HS256':
                return settings.PROJECT_SECRET_KEY
            case _:
                raise errors.UnsupportedAlgorithmError()
    
    def _get_rsa_key(self, private: bool=False) -> str | bytes:
        file_type: str = "private" if private else "public"
        with open(f"{Path().parent.parent}/keys/{file_type}.pem", "rb") as file:
            rsa_key: bytes | str = file.read()
        return rsa_key
    