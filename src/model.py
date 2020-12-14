from datetime import datetime

from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, String,DateTime,create_engine
from sqlalchemy.ext.declarative import declarative_base
from BnuAutoLogin.configs.sql_config import DB_URI

Base = declarative_base()


class Users(Base):
    """用户信息
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    account_number = Column(String(50))
    password_hash = Column(String(128))
    # 用户创建时间
    create_time = Column(DateTime, default=datetime.now)

    # 密码散列
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # 密码验证
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
