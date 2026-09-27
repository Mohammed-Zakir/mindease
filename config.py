import os


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = "sqlite:///mindease.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False