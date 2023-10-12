from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    func,
)

from src.database import Base


class AuthRefreshToken(Base):
    __tablename__ = "auth_refresh_tokens"

    id = Column("id", Integer, Identity(), primary_key=True)
    user_id = Column(
        "user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False
    )
    refresh_token = Column("refresh_token", String, nullable=False)
    expires_at = Column("expires_at", DateTime, nullable=False)
    created_at = Column(
        "created_at", DateTime, server_default=func.now(), nullable=False
    )
    updated_at = Column("updated_at", DateTime, onupdate=func.now())

    def __repr__(self):
        return f"({self.id} {self.first_name} {self.last_name})"
