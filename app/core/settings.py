from pydantic import BaseSettings, validator

"""
    :class _Settings - specify all project settings from environment 
    variables.
"""
class _Settings(BaseSettings):
    PRODUCTION: bool
    
    """
        :constants PROJECT - set up environment variables por project
        general information.
    """
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    PROJECT_VERSION: str | None
    
    """
        :constants MONGO - specify mongo credentials for DB connection.
    """
    MONGO_PORT: str | int
    MONGO_HOST: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_URI: str
    MONGO_DATABASE: str
    
    """
        :constants SECRET - project secret keys
    """
    PROJECT_SECRET_KEY: str
    
    """
        :constants SMTP - credentials for SMTP server.
    """
    SMTP_HOSTNAME: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
    """
        :validators - specify if the environment variables are correct.
    """
    @validator("MONGO_URI", pre=True, always=True)
    def assemble_uri(cls, value: str | dict[str, str | object]) -> str:
        if isinstance(value, str):
            return value
        else:
            return f"mongodb+srv://{cls.MONGO_USERNAME}:{cls.MONGO_PASSWORD}@{cls.MONGO_HOST}/?retryWrites=true&w=majority"
    
    class Config:
        env_file = ".env"
        env_encoding = "utf-8"
        case_sensitive: bool = True

settings = _Settings()
