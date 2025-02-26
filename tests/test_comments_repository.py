import datetime as dt
import os
from pathlib import Path

from src.comments_repository import SQLLiteCommentsRepository
from src.domain import UnregisteredComment, Comment


def test_adding_empty_comments():
    try:
        comments_repository = SQLLiteCommentsRepository(Path("test_repository.db"))
        retrieved = comments_repository.comments("dbz")
        assert retrieved == []
    finally:
        os.remove("test_repository.db")


def test_adding_and_retrieving_two_comments():
    try:

        comments_repository = SQLLiteCommentsRepository(Path("test_repository.db"))
        comments_repository.add_comment(UnregisteredComment("dbz", "Tom", "t@tom.io", "Salut !", dt.date(2024, 12, 10)))
        comments_repository.add_comment(
            UnregisteredComment("dbz", "Mike", "m@mike.io", "Salut c'est Mike!", dt.date(2024, 12, 11))
        )
        retrieved = comments_repository.comments("dbz")
        assert retrieved == [
            Comment(1, "dbz", "Tom", "t@tom.io", "Salut !", dt.date(2024, 12, 10)),
            Comment(2, "dbz", "Mike", "m@mike.io", "Salut c'est Mike!", dt.date(2024, 12, 11)),
        ]
    finally:
        os.remove("test_repository.db")
