import datetime

from sqlalchemy import Column, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import LargeBinary
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    hash_password = Column(LargeBinary, nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    posts = relationship(
        "UserModel",
        back_populates="user",
        uselist=True
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),

    )
