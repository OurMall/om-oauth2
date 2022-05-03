import datetime
from fastapi import HTTPException
from authlib.jose import jwt, errors
from authlib.common.encoding import to_bytes, to_unicode

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
                key=self._load_key(private_key=True),
                check=True
            )
            token = to_unicode(encoded)
        except Exception as e:
            raise ValueError('Cannot encode the payload', e)
        else:
            return token
    
    def decode(
        self,
        encoded: str | bytes,
        validate: bool | None
    ) -> object:
        if not isinstance(encoded, bytes):
            encoded = to_bytes(encoded)
        key = self._load_key(private_key=True)
        dot_count: int = encoded.count(b'.')
        if dot_count == 2:
            key = self._load_key(private_key=False)
        try:
            payload: dict[str, object] = jwt.decode(
                s=encoded,
                key=key
            )
            if validate:
                payload.validate(
                    leeway=datetime.timedelta(minutes=11).total_seconds()
                )
        except errors.ExpiredTokenError:
            raise HTTPException(status_code=401, detail="Token expired")
        except errors.BadSignatureError:
            raise HTTPException(status_code=401, detail="Bad token signature")
        except errors.DecodeError:
            raise HTTPException(status_code=401, detail="Fail to decode token")
        else:
            return payload
    
    def revoke(self):
        pass
    
    def _load_key(
        self, 
        private_key: bool=False
    ):
        def load_key(header: dict[str, object], payload: dict[str, object]):
            match header['alg']:
                case 'RS256' | 'RSA-OAEP-256':
                    if private_key:
                        key: bytes | str = self._get_rsa_key(private=True)
                    else:
                        key = self._get_rsa_key()
                    return key
                case 'HS256':
                    return settings.PROJECT_SECRET_KEY
                case _:
                    raise errors.UnsupportedAlgorithmError()
        return load_key
    
    def _get_rsa_key(self, private: bool=False) -> str | bytes:
        file_type: str = "private" if private else "public"
        with open(f"app/keys/{file_type}.pem", "rb") as file:
            rsa_key: bytes | str = file.read()
        return rsa_key
    