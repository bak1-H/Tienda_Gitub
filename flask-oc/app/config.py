import os

class Config:
    # estudiante: SECRET_KEY y DATABASE_URL se leen de variables o .env
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    # fallback correcto a sqlite local si no hay DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
