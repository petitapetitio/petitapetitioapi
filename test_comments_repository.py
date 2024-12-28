import datetime
import os
import sqlite3
import datetime as dt
from comments_repository import CommentsRepository
from domain import UnregisteredComment, Comment


def test_repository():
    try:
        connection = sqlite3.Connection("test_repository.db")
        comments_repository = CommentsRepository(connection)
        comments_repository.add_comment(UnregisteredComment("Tom", "t@tom.io", "Salut !", dt.date(2024, 12, 10)))
        comments_repository.add_comment(
            UnregisteredComment("Mike", "m@mike.io", "Salut c'est Mike!", dt.date(2024, 12, 11))
        )
        retrieved = comments_repository.comments()
        assert retrieved == [
            Comment(1, "Tom", "t@tom.io", "Salut !", dt.date(2024, 12, 10)),
            Comment(2, "Mike", "m@mike.io", "Salut c'est Mike!", dt.date(2024, 12, 11)),
        ]
    finally:
        os.remove("test_repository.db")
