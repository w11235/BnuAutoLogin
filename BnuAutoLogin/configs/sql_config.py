import sqlite3

from BnuAutoLogin.configs import settings
from sqlalchemy import create_engine

DATABASE = settings.DATA_DIR / "auto_login.db"
DB_URI= f"sqlite:///{DATABASE}"
engine = create_engine(DB_URI)

# flask_sqlalchemy 配置参数
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
