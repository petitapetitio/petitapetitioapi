import datetime
import sqlite3
from abc import ABCMeta, abstractmethod
from pathlib import Path

import psycopg

from src.domain import UnregisteredComment, Comment, Message


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


class PostgresCommentsRepository(CommentsRepository):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        with psycopg.connect(self._connection_string) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS comments (
                    id SERIAL PRIMARY KEY,
                    post_slug text NOT NULL,
                    author_name text NOT NULL CHECK(length(author_name) < 100),
                    author_email text NOT NULL CHECK(length(author_email) < 250),
                    message text NOT NULL CHECK(length(message) < 1000),
                    sent_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_comments_post_slug ON comments(post_slug);
                
                CREATE TABLE IF NOT EXISTS messages (
                    author_name text NOT NULL CHECK(length(author_name) < 100),
                    author_email text NOT NULL CHECK(length(author_email) < 250),
                    message text NOT NULL CHECK(length(message) < 1000),
                    sent_at timestamp NOT NULL 
                );
                """
            )

    def add_message(self, message: Message):
        with psycopg.connect(self._connection_string) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages (author_name, author_email, message, sent_at) VALUES (%s, %s, %s, %s)",
                (message.author_name, message.author_email, message.message, message.sent_at),
            )

    def messages(self) -> list[Message]:
        with psycopg.connect(self._connection_string) as conn:
            cur = conn.cursor()
            res = cur.execute("SELECT author_name, author_email, message, sent_at FROM messages")
            messages = [Message(author_name=r[0], author_email=r[1], message=r[2], sent_at=r[3]) for r in res.fetchall()]
            return messages

    def add_comment(self, comment: UnregisteredComment):
        with psycopg.connect(self._connection_string) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO comments (post_slug, author_name, author_email, message, sent_at) values (%s, %s, %s, %s, %s)",
                (comment.post_slug, comment.author_name, comment.author_email, comment.message, comment.sent_at),
            )

    def comments(self, post_slug: str) -> list[Comment]:
        with psycopg.connect(self._connection_string) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, post_slug, author_name, author_email, message, sent_at FROM comments where post_slug = %s",
                (post_slug,),
            )
            results = list(cur.fetchall())
            return [
                Comment(
                    comment_id=r[0],
                    post_slug=r[1],
                    author_name=r[2],
                    author_email=r[3],
                    message=r[4],
                    sent_at=r[5],
                )
                for r in results
            ]
