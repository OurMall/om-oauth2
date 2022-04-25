from pydantic import BaseSettings, validator

"""
    :class _Settings - specify all project settings from environment 
    variables.
"""
class _Settings(BaseSettings):
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
    MONGO_URI: str
    MONGO_DATABASE: str
    
    """
        :constants SECRET - project secret keys
    """
    PROJECT_SECRET_KEY: str
    
    """
        :validators - specify if the environment variables are correct.
    """
    @validator("MONGO_URI", pre=True, always=True)
    def assemble_uri(cls, value: str | dict[str, str | object]) -> str:
        if isinstance(value, str):
            return value
        else:
            return f"mongodb://localhost:{value.get('port')}"
    
    class Config:
        env_file: str = ".env.local"
        case_sensitive: bool = True

settings = _Settings()