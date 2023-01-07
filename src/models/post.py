import datetime

from sqlalchemy import Column, ForeignKeyConstraint, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class PostModel(BaseModel):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    inserted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    user = relationship(
        "UserModel",
        back_populates="posts",
        uselist=False
    )

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (user_id,),
            ("user.id",),
        )
    )
