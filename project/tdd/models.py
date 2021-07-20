from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from project.database import Base


class Member(Base):

    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)

    avatar = Column(String(256), nullable=False)
    avatar_thumbnail = Column(String(256), nullable=True)
