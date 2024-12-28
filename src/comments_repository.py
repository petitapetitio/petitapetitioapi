import datetime
import sqlite3
from pathlib import Path

from src.domain import UnregisteredComment, Comment


class CommentsRepository:
    def __init__(self, db_name: Path):
        self._db_name = db_name
        self._initialize_tables()

    def _initialize_tables(self):
        print(self._db_name)
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Comments (Id INT, Author TEXT, Email TEXT, Message TEXT, Date TEXT)"
            )

    def add_comment(self, comment: UnregisteredComment):
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
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
        with sqlite3.connect(self._db_name) as con:
            cursor = con.cursor()
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

