import datetime as dt
import os
from pathlib import Path

from src.comments_repository import CommentsRepository
from src.domain import UnregisteredComment, Comment


def test_adding_and_retrieving_two_comments():
    try:

        comments_repository = CommentsRepository(Path("test_repository.db"))
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
