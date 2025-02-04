from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, unique=True, index=True)
    dob = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    created_at = Column(Date, nullable=False)

    # Связываем с Name
    name = relationship("Name", back_populates="user", uselist=False)
    # login
    login = relationship("Login", back_populates="user", uselist=False)


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
    __tablename__ = 'names'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))
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
    __tablename__ = 'logins'

    uuid = Column(
        String,
        primary_key=True,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    user = relationship("User", back_populates="login")

    def __repr__(self):
        return f"Login(uuid={self.uuid}"