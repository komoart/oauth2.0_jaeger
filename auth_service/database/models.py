import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum

from core.utils import DeviceType
from .postgresql import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(
        String(30),
        unique=True,
        nullable=False,
    )
    password = Column(
        String(30),
        nullable=False,
    )
    authlogs = relationship(
        "AuthLogs",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    def __repr__(self):
        return f'<User {self.login}>'


def create_partition(target, connection, **kw) -> None:
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_logs_smart" PARTITION OF "auth_logs" FOR VALUES IN ('SMART');"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_logs_mobile" PARTITION OF "auth_logs" FOR VALUES IN ('MOBILE');"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_logs_web" PARTITION OF "auth_logs" FOR VALUES IN ('WEB');"""
    )


class AuthLogs(Base):
    __tablename__ = 'auth_logs'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        })

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id, ondelete="CASCADE"),
        nullable=False,
    )
    user_agent = Column(
        String(30),
        nullable=False,
    )
    log_type = Column(
        String(30),
        nullable=True,
    )
    datetime = Column(
        DateTime,
        nullable=False,
        default=datetime.now()
    )
    ip_address = Column(
        String(30),
        nullable=True,
    )
    user = relationship(
        "Users",
        back_populates="authlogs",
    )
    user_device_type = Column(SQLEnum(DeviceType), primary_key=True)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(30),
        unique=True,
        nullable=False,
    )

    def __repr__(self):
        return f'<Roles {self.name}>'


class UsersRoles(Base):
    __tablename__ = 'users_roles'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id),
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Roles.id),
    )


class Token(Base):
    __tablename__ = 'token'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    token = Column(
        String(128),
        unique=True,
        nullable=False,
    )
    token_type = Column(
        String(100),
    )


class SocialUser(Base):
    __tablename__ = 'social_user'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        String(256),
        nullable=False,
    )
    email = Column(
        String(256),
        nullable=False,
    )


class SocialAccount(Base):
    __tablename__ = "social_accounts"
    __table_args__ = (
        UniqueConstraint("social_id", "social_name", name="social_uc"),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    user = relationship(
        Users,
        backref=SQLAlchemy().backref("social_accounts", lazy=True),
    )
    social_id = Column(
        String(255),
        nullable=False,
    )
    social_name = Column(
        String(255),
        nullable=False,
    )

    def __str__(self) -> str:
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
