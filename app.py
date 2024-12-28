import datetime
from configparser import ConfigParser
from pathlib import Path

from flask import Flask, Response
from flask import request
from flask_cors import CORS
from markupsafe import escape

from src.comments_repository import CommentsRepository
from src.domain import UnregisteredComment

app = Flask(__name__)

config = ConfigParser()
config.read("settings.ini")
db = Path(config["general"]["db_path"])
comments_repository = CommentsRepository(db)
origins = config["general"]["cors_origins"].split(",")
CORS(app, origins=origins)


@app.route('/comments/<post_slug>')
def get_comments(post_slug: str):
    print("get_comments", post_slug)

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
    print(request.values)
    comment = UnregisteredComment(
        escape(request.form['post_slug']),
        escape(request.form['author_name']),
        escape(request.form['author_email']),
        escape(request.form['message']),
        datetime.date.today(),
    )
    comments_repository.add_comment(comment)
    return Response(status=200)

