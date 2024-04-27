import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    
    # Database
    DB_USER: str = os.getenv('MYSQL_USER')
    DB_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
    DB_NAME: str = os.getenv('MYSQL_DB')
    DB_HOST: str = os.getenv('MYSQL_SERVER')
    DB_PORT: str = os.getenv('MYSQL_PORT')
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:%s@{DB_HOST}:{DB_PORT}/{DB_NAME}" % quote_plus(DB_PASSWORD)
    
    # JWT 
    JWT_SECRET: str = os.getenv('JWT_SECRET', '709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    JWT_TOKEN_EXPIRE: int = os.getenv('JWT_TOKEN_EXPIRE', 30)
    JWT_REFRESH_TOKEN_EXPIRE: int = os.getenv('JWT_REFRESH_TOKEN_EXPIRE', 60)
    #mail
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('EMAIL_APP_PASSWORD')
    MAIL_FROM: str = os.getenv('MAIL_USERNAME')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', 587))
    MAIL_SERVER: str = os.getenv('MAIL_SERVER', "smtp.gmail.com")
    USE_CREDENTIALS: bool = os.getenv('USE_CREDENTIALS', "True").lower() == "true"
    MAIL_STARTTLS: bool = os.getenv('MAIL_STARTTLS', "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv('MAIL_SSL_TLS', "False").lower() == "true"
    #google
    CLIENT_ID: str  = os.getenv('GOOGLE_CLIENT_ID')
    CLIENT_SECRET: str  = os.getenv('GOOGLE_CLIENT_SECRET')
    
def get_settings() -> Settings:
    return Settings()