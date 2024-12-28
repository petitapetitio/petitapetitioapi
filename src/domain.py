import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Comment:
    comment_id: int
    author_name: str
    author_email: str
    message: str
    date: datetime.date


@dataclass(frozen=True)
class UnregisteredComment:
    author_name: str
    author_email: str
    message: str
    date: datetime.date
