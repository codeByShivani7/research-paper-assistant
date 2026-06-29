from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Research Paper Intelligent Assistant"
    app_env: str = "local"

    class Config:
        env_file = ".env"


settings = Settings()