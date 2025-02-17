import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Comment:
    comment_id: int
    post_slug: str
    author_name: str
    author_email: str
    message: str
    sent_at: datetime.datetime


@dataclass(frozen=True)
class UnregisteredComment:
    post_slug: str
    author_name: str
    author_email: str
    message: str
    sent_at: datetime.datetime


@dataclass(frozen=True)
class Message:
    author_name: str
    author_email: str
    message: str
    sent_at: datetime.datetime
