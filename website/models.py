import sqlalchemy
db: sqlalchemy
from types import FunctionType
from website import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, DateTime
from sqlalchemy.ext.mutable import *

import time, datetime

class User(db.Model, UserMixin):
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    avatar: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    codeforces_username: Mapped[str] = mapped_column(unique=True, nullable=False)
    rating: Mapped[int] = mapped_column(default=1000)

    def __repr__(self):
        return f"User({self.id}, {self.name})"

class FreeProblem(db.Model):
    oj: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[str] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now, onupdate=datetime.datetime.now)

    title: Mapped[str] = mapped_column(default="No title")
    data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSON), default={})
    description: Mapped[str] = mapped_column(default="")
    translated: Mapped[str] = mapped_column(default="")

    rating: Mapped[str] = mapped_column(nullable=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


