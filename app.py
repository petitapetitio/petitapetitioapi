import datetime
import sys
from configparser import ConfigParser
from dataclasses import asdict
from pathlib import Path

from flask import Flask, Response
from flask import request
from flask_cors import CORS
from markupsafe import escape

from src.comments_repository import CommentsRepository
from src.domain import UnregisteredComment, Message
from src.email_client import DisabledEmailClient, SMTPEmailClient

app = Flask(__name__)

config = ConfigParser()
config.read("settings.ini")
db = Path(config["general"]["db_path"])
comments_repository = CommentsRepository(db)
origins = config["general"]["cors_origins"].split(",")
is_local = sys.platform.startswith("darwin")
email_client = DisabledEmailClient() if is_local else SMTPEmailClient()
CORS(app, origins=origins)


@app.route('/comments/<post_slug>')
def get_comments(post_slug: str):
    comments = comments_repository.comments(post_slug)

    formatted = ""
    for comment in comments:
        formatted += f"""
<li id="comment-{comment.comment_id}">
<cite>{comment.author_name} ({comment.date}) <a href="#comment-{comment.comment_id}">#</a></cite>
<p>{comment.message}</p>
</li>"""

    return f"""
        <div id="commentlist">
            <ol>
                {formatted}
            </ol>
        </div>
"""


@app.route('/comment', methods=['POST'])
def add_comment():
    comment = UnregisteredComment(
        escape(request.form['post_slug']),
        escape(request.form['author_name']),
        escape(request.form['author_email']),
        escape(request.form['message']),
        datetime.date.today(),
    )
    comments_repository.add_comment(comment)
    email_client.notify_new_comment(comment)
    return Response(status=200)


@app.route('/message', methods=['POST'])
def send_message():
    message = Message(
        escape(request.form['author_name']),
        escape(request.form['author_email']),
        escape(request.form['message']),
        datetime.datetime.now(),
    )
    comments_repository.add_message(message)
    email_client.notify_new_message(message)
    return Response(status=200)


@app.route('/messages')
def get_messages():
    if request.remote_addr != '127.0.0.1':
        return "Access denied", 403

    message = comments_repository.messages()
    return [asdict(m) for m in message]

