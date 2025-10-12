import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user1:password123@localhost:5432/meeting_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt")  
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

