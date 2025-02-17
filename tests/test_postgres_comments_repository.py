from datetime import date, datetime

import psycopg

from src.comments_repository import PostgresCommentsRepository
from src.domain import UnregisteredComment, Comment, Message


def get_test_db_connection():
    with psycopg.connect("dbname=postgres") as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS petitapetitio_tests_db")
            cur.execute("CREATE DATABASE petitapetitio_tests_db")

    return psycopg.connect("dbname=petitapetitio_tests_db")  ## user=petitapetitio_tests_user")


def test_adding_empty_comments():
    with get_test_db_connection() as conn:
        comments_repository = PostgresCommentsRepository(conn)
        retrieved = comments_repository.comments("dbz")
        assert retrieved == []


def test_adding_and_retrieving_two_comments():
    with get_test_db_connection() as conn:
        comments_repository = PostgresCommentsRepository(conn)
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
        retrieved = comments_repository.comments("dbz")
        assert retrieved == [
            Comment(1, "dbz", "Tom", "t@tom.io", "Salut !", date(2024, 12, 10)),
            Comment(2, "dbz", "Mike", "m@mike.io", "Salut c'est Mike!", date(2024, 12, 11)),
        ]


def test_adding_and_retrieving_message():
    with get_test_db_connection() as conn:
        repo = PostgresCommentsRepository(conn)
        message = Message("alex", "tests@petitapetit.io", "hey", datetime.now())
        repo.add_message(message)
        assert repo.messages() == [message]
