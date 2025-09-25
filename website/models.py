import sqlalchemy
db: sqlalchemy
from types import FunctionType
from website import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, DateTime
from sqlalchemy.ext.mutable import *

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    avatar: Mapped[str] = mapped_column(nullable=True)
    nickname: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(default=1000)

    def __repr__(self):
        return f"User({self.id}, {self.username})"

class FreeProblem(db.Model):
    oj: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[str] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[int] = mapped_column(default=0)

    title: Mapped[str] = mapped_column(default="No title")
    data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSON), default={})
    description: Mapped[str] = mapped_column(default="")
    translated: Mapped[str] = mapped_column(default="")

    rating: Mapped[str] = mapped_column(nullable=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


