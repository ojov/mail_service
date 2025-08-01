import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    MAILTRAP_API_TOKEN: str = Field("", env="MAILTRAP_API_TOKEN")
    MAILTRAP_FROM_EMAIL: EmailStr = Field("victorojo007@gmail.com",env="SMTP_HOST")
    MAILTRAP_FROM_NAME: Optional[str] = Field("Profile App", env="MAILTRAP_FROM_NAME")
    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()


class MailBody(BaseModel):
    sender_name: str
    sender_email: str
    subject: str
    body: str
    html: bool = True

    model_config = ConfigDict(extra="forbid")
