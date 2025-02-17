from datetime import date, datetime

import psycopg

from src.comments_repository import PostgresCommentsRepository
from src.domain import UnregisteredComment, Comment, Message


def reset_db():
    with psycopg.connect("dbname=postgres") as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS petitapetitio_tests_db")
            cur.execute("CREATE DATABASE petitapetitio_tests_db")


def get_test_db_connection() -> str:
    return "postgresql://lxnd@localhost:5432/petitapetitio_tests_db"


def test_adding_empty_comments():
    reset_db()
    comments_repository = PostgresCommentsRepository(get_test_db_connection())
    retrieved = comments_repository.comments("dbz")
    assert retrieved == []


def test_adding_and_retrieving_two_comments():
    reset_db()
    comments_repository = PostgresCommentsRepository(get_test_db_connection())
    comments_repository.add_comment(
        UnregisteredComment(
            "dbz",
            "Tom",
            "t@tom.io",
            "Salut !",
            date(2024, 12, 10),
        )
    )
    comments_repository.add_comment(
        UnregisteredComment(
            "dbz",
            "Mike",
            "m@mike.io",
            "Salut c'est Mike!",
            date(
                2024,
                12,
                11,
            ),
        )
    )

    comments_repository = PostgresCommentsRepository(get_test_db_connection())
    retrieved = comments_repository.comments("dbz")
    assert retrieved == [
        Comment(1, "dbz", "Tom", "t@tom.io", "Salut !", date(2024, 12, 10)),
        Comment(2, "dbz", "Mike", "m@mike.io", "Salut c'est Mike!", date(2024, 12, 11)),
    ]


def test_adding_and_retrieving_message():
    reset_db()
    repo = PostgresCommentsRepository(get_test_db_connection())
    message = Message("alex", "tests@petitapetit.io", "hey", datetime.now())
    repo.add_message(message)

    repo = PostgresCommentsRepository(get_test_db_connection())
    assert repo.messages() == [message]
