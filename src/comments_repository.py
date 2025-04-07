import datetime
import sqlite3
from abc import ABCMeta, abstractmethod
from pathlib import Path

from src.domain import UnregisteredComment, Comment, Message, Email


class CommentsRepository(metaclass=ABCMeta):
    @abstractmethod
    def add_message(self, message: Message):
        pass

    @abstractmethod
    def messages(self) -> list[Message]:
        pass

    @abstractmethod
    def add_comment(self, comment: UnregisteredComment):
        pass

    @abstractmethod
    def comments(self, post_slug: str) -> list[Comment]:
        pass

    @abstractmethod
    def add_email(self, email: Email):
        raise NotImplementedError

    @abstractmethod
    def emails(self) -> list[Email]:
        raise NotImplementedError


class SQLLiteCommentsRepository(CommentsRepository):
    def __init__(self, db_name: Path):
        self._db_name = db_name
        self._initialize_tables()

    def _initialize_tables(self):
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Comments (Id INT, PostSlug TEXT, Author TEXT, Email TEXT, Message TEXT, Date TEXT)"
            )
            cursor.execute("CREATE TABLE IF NOT EXISTS Messages (Author TEXT, Email TEXT, Message TEXT, Date TEXT)")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                Id INT UNIQUE, 
                Name TEXT, 
                Email TEXT PRIMARY KEY
            )
            """)

    def add_message(self, message: Message):
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO Messages(Author, Email, Message, Date) VALUES (?, ?, ?, ?)",
                (
                    message.author_name,
                    message.author_email,
                    message.message,
                    message.sent_at.isoformat(),
                ),
            )

    def messages(self) -> list[Message]:
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT Author, Email, Message, Date FROM Messages")
            raw_comments = cursor.fetchall()
            return [
                Message(
                    author_name=c[0],
                    author_email=c[1],
                    message=c[2],
                    sent_at=datetime.datetime.fromisoformat(c[3]),
                )
                for c in raw_comments
            ]

    def add_comment(self, comment: UnregisteredComment):
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT max(Id) FROM Comments")
            id_max = cursor.fetchone()[0]
            identifier = id_max + 1 if id_max is not None else 1

            cursor.execute(
                "INSERT INTO Comments(Id, PostSlug, Author, Email, Message, Date) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    identifier,
                    comment.post_slug,
                    comment.author_name,
                    comment.author_email,
                    comment.message,
                    comment.sent_at.isoformat(),
                ),
            )

    def comments(self, post_slug: str) -> list[Comment]:
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT Id, Author, Email, Message, Date FROM Comments WHERE PostSlug = ?", (post_slug,))
            raw_comments = cursor.fetchall()
            comments = [
                Comment(
                    comment_id=c[0],
                    post_slug=post_slug,
                    author_name=c[1],
                    author_email=c[2],
                    message=c[3],
                    sent_at=datetime.datetime.fromisoformat(c[4]),
                )
                for c in raw_comments
            ]
        return comments

    def add_email(self, email: Email):
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT max(Id) FROM Users")
            id_max = cursor.fetchone()[0]
            identifier = id_max + 1 if id_max is not None else 1

            cursor.execute(
                "INSERT INTO Users(Id, Name, Email) VALUES (?, ?, ?) ON CONFLICT(Email) DO NOTHING",
                (
                    identifier,
                    "",
                    email._email,
                ),
            )

    def emails(self) -> list[Email]:
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT Email FROM Users")
            raw_users = cursor.fetchall()
            emails = [Email(e[0]) for e in raw_users]
        return emails


