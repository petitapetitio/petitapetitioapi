import psycopg

from src.comments_repository import CommentsRepository
from src.domain import Message, UnregisteredComment, Comment


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
            messages = [
                Message(author_name=r[0], author_email=r[1], message=r[2], sent_at=r[3]) for r in res.fetchall()
            ]
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
