import datetime
from sqlite3 import Connection
from typing import Iterable

from domain import UnregisteredComment, Comment


class CommentsRepository:
    def __init__(self, connection, current_comments: Iterable[Comment] = ()):
        self._connection: Connection = connection
        self._comments: list[Comment] = list(current_comments)
        self._initialize_tables()

    def _initialize_tables(self):
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Comments (Id INT, Author TEXT, Email TEXT, Message TEXT, Date TEXT)"
            )

    def add_comment(self, comment: UnregisteredComment):
        comment_id = len(self._comments) + 1
        comment = Comment(
            comment_id=comment_id,
            author_name=comment.author_name,
            author_email=comment.author_email,
            message=comment.message,
            date=comment.date,
        )
        self._comments.append(comment)

        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute("SELECT max(Id) FROM Comments")
            id_max = cursor.fetchone()[0]
            identifier = id_max + 1 if id_max is not None else 1

            cursor.execute(
                "INSERT INTO Comments(Id, Author, Email, Message, Date) VALUES (?, ?, ?, ?, ?)",
                (
                    identifier,
                    comment.author_name,
                    comment.author_email,
                    comment.message,
                    comment.date.strftime("%Y-%m-%d"),
                ),
            )

    def comments(self) -> list[Comment]:
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute("SELECT Id, Author, Email, Message, Date FROM Comments")
            raw_comments = cursor.fetchall()
            comments = [
                Comment(
                    comment_id=c[0],
                    author_name=c[1],
                    author_email=c[2],
                    message=c[3],
                    date=datetime.datetime.strptime(c[4], "%Y-%m-%d").date(),
                )
                for c in raw_comments
            ]
        return comments

