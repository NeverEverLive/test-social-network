import datetime

from sqlalchemy import Column, ForeignKeyConstraint, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy.types import Integer
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.postgres.base import BaseModel


class PostModel(BaseModel):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    text = Column(String, nullable=False)
    like = Column(Integer, nullable=False, default=0)
    dislike = Column(Integer, nullable=False, default=0)
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
