from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Identity,
    Integer,
    String,
    func,
)

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, Identity(), primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)
    phone_number = Column("phone_number", String, nullable=True)
    password = Column("password", String, nullable=False)
    is_admin = Column("is_admin", Boolean, server_default="false", nullable=False)
    created_at = Column(
        "created_at", DateTime, server_default=func.now(), nullable=False
    )
    updated_at = Column("updated_at", DateTime, onupdate=func.now())

    def __repr__(self):
        return f"({self.id} {self.first_name} {self.last_name})"
