from datetime import timedelta
from os import environ

database_url = environ["DATABASE"]


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{database_url}/authentication"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
