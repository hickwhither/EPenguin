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
    id: Mapped[str] = mapped_column(primary_key=True)
    oj: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[int] = mapped_column(default=0)

    title: Mapped[str] = mapped_column(default="No title")
    description: Mapped[str] = mapped_column(default="")
    translated: Mapped[str] = mapped_column(default="")

    timelimit: Mapped[int] = mapped_column(default=0)
    memorylimit: Mapped[int] = mapped_column(default=0)
    input: Mapped[str] = mapped_column(default="")
    output: Mapped[str] = mapped_column(default="")


    rating: Mapped[str] = mapped_column(nullable=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


