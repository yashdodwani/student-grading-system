from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL",
                                  "postgresql://sgs_owner:npg_4YZpodaRP5Qu@ep-polished-cloud-a1qvxquj-pooler.ap-southeast-1.aws.neon.tech/sgs?sslmode=require")

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application settings
    APP_NAME: str = "Student Grading System"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()