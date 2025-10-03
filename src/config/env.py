from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=3000)
    api_prefix: str = Field(default="/api/v1")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 