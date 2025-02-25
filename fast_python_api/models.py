from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from typing import Any
import uuid


Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.
    Contains information about a user such as date of birth, city,
    email and etc.
    """
    __tablename__ = 'users'

    id = Column(
        String,
        primary_key=True,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    dob = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # Связываем с Name
    name = relationship(
        "Name",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan"
    )
    # login
    login = relationship(
        "Login",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "dob": self.dob,
            "city": self.city,
            "email": self.email,
            "created_at": self.created_at,
            "name": {
                "title": self.name.title,
                "first_name": self.name.first_name,
                "last_name": self.name.last_name,
            },
            "login": {
                "uuid": self.login.uuid,
                "role": self.login.role,
                "username": self.login.username,
                "password": self.login.password,
            },
        }

    def __repr__(self):
        name_repr = (
            f'{self.name.title} {self.name.first_name} {self.name.last_name}'
        )
        return (
            f"User(id={self.id}, "
            f"name={name_repr}, "
            f"email={self.email}, "
            f"city={self.city}, "
            f"dob={self.dob})"
        )


class Name(Base):
    """
    Represents a name in the system.
    Contains information about a user such as title, first name,
    last name and etc.
    """
    __tablename__ = 'names'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        String, ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    title = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Связываем с User
    user = relationship("User", back_populates="name")

    def __repr__(self):
        return (
            f"Name(id={self.id}, "
            f"title={self.title}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name})"
        )


class Login(Base):
    """
    Represents a login in the system.
    Contains information about a user such as username, password and etc.
    """
    __tablename__ = 'logins'

    uuid = Column(
        String,
        ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(50), nullable=False, default="user")

    user = relationship("User", back_populates="login")

    def __repr__(self):
        return f"Login(uuid={self.uuid})"
