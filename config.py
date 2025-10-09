import os

class Config:
    SECRET_KEY = 'pr0gr4m4c10nw3b'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}