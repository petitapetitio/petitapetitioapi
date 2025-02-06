import datetime as dt

import psycopg

from src.comments_repository import CommentsRepository
from src.domain import UnregisteredComment, Comment, Message


def get_test_db_connection():
    with psycopg.connect("dbname=postgres") as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS petitapetitio_tests_db")
            cur.execute("CREATE DATABASE petitapetitio_tests_db")

    return psycopg.connect("dbname=petitapetitio_tests_db")  ## user=petitapetitio_tests_user")


class PostgresCommentsRepository(CommentsRepository):
    def __init__(self, connection: psycopg.Connection):
        self._connection = connection
        with connection.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS comments (
                    id SERIAL,
                    post_slug text,
                    author_name text,
                    author_email text,
                    message text,
                    created_on date DEFAULT CURRENT_DATE
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    author_name text,
                    author_email text,
                    message text,
                    created_on date
                )
                """
            )

    def add_message(self, message: Message):
        pass

    def messages(self) -> list[Message]:
        pass

    def add_comment(self, comment: UnregisteredComment):
        with self._connection.cursor() as cur:
            cur.execute(
                "INSERT INTO comments (post_slug, author_name, author_email, message, created_on) values (%s, %s, %s, %s, %s)",
                (comment.post_slug, comment.author_name, comment.author_email, comment.message, comment.date),
            )

    def comments(self, post_slug: str) -> list[Comment]:
        with self._connection.cursor() as cur:
            cur.execute(
                "SELECT id, post_slug, author_name, author_email, message, created_on FROM comments where post_slug = %s",
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
                    date=r[5],
                )
                for r in results
            ]


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
                dt.date(2024, 12, 10),
            )
        )
        comments_repository.add_comment(
            UnregisteredComment(
                "dbz",
                "Mike",
                "m@mike.io",
                "Salut c'est Mike!",
                dt.date(
                    2024,
                    12,
                    11,
                ),
            )
        )
        retrieved = comments_repository.comments("dbz")
        assert retrieved == [
            Comment(1, "dbz", "Tom", "t@tom.io", "Salut !", dt.date(2024, 12, 10)),
            Comment(2, "dbz", "Mike", "m@mike.io", "Salut c'est Mike!", dt.date(2024, 12, 11)),
        ]
