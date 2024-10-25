import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.environ['APP_NAME']
    SECRET_KEY = os.environ['SECRET_KEY']
    ALCHEMICAL_DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
