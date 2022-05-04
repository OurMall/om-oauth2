from passlib.context import CryptContext

class AuthService:
    
    password_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )
    
    @classmethod
    def verify_password(cls, plain: str, hash: str | bytes) -> bool:
        return cls.password_context.verify(plain, hash)
    
    @classmethod
    def hash_password(cls, plain: str) -> str | bytes:
        return cls.password_context.hash(plain)