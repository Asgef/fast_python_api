from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)

    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    timezone = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)
    phone = Column(String)

    created_at = Column(Date, nullable=False)

    def __repr__(self):
        return (
            f"User(id={self.id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"dob={self.dob})"
        )
