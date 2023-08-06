# coding: utf-8
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config.settings import SettingsFactory, inject_settings

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True, index=True)
    email = Column(String(255), unique=True, comment='邮箱')
    hashed_password = Column(String(255), comment='密码')
    is_active = Column(TINYINT(1), comment='是否激活')


class UserModel(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_active: bool

    class Config:
        orm_mode = True


class Item(Base):
    __tablename__ = 'items'

    id = Column(INTEGER(11), primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(ForeignKey('users.id'), index=True)

    owner = relationship('User')


if __name__ == '__main__':
    # 指定表 导出 model
    # sqlacodegen mysql+pymysql://user:password@127.0.0.1:3306/dbname --outfile=models.py
    inject_settings.set_default_log_dir(r"./logs")
    s = SettingsFactory.default()
    db = s.datasource
    with db.session as session:
        u = session.query(User).first()
        user = UserModel.from_orm(u)
        print(user)
    print(s.redis.session.hget("test", "a"))
    print(s.es.session.info())
