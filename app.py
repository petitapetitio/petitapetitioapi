import datetime
from configparser import ConfigParser
from pathlib import Path

from flask import Flask
from flask import request
from markupsafe import escape

from src.comments_repository import CommentsRepository
from src.consts import lorel_ipsum
from src.domain import UnregisteredComment

app = Flask(__name__)

config = ConfigParser()
config.read("settings.ini")
db = Path(config["general"]["db_path"])
print(db)
comments_repository = CommentsRepository(db)


@app.route('/comments/<int:post_id>')
def get_comments(post_id: int):
    print("get_comments", post_id)

    comments = comments_repository.comments(post_id)

    formatted = ""
    for comment in comments:
        formatted += f"""
<li id="comment-{comment.comment_id}">
<cite>{comment.author_name} ({comment.date}) <a href="#comment-{comment.comment_id}">#</a></cite>
<p>{comment.message}</p>
</li>"""

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quote of the Day</title>
        <style>
            body, html {{
                height: 100%;
                margin: 0;
                font-family: Verdana, sans-serif, system-ui;
            }}
            
            body {{
                background-color: #F7F7F7; /* Wheat color for a paper-like background */
                color: #333; /* Dark gray color for text which is easier on the eyes */
                
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-direction: column;
                padding: 24px;
                text-align: center;
                height: calc(100vh - 48px);
            }}
        </style>
    </head>
    <body>
    
        {lorel_ipsum}

        <div id="commentlist">
            <ol>
                {formatted}
            </ol>
        </div>
        
        {lorel_ipsum}
    </body>
    </html>
    """


@app.route('/comment', methods=['POST'])
def add_comment():
    print(request.values)
    comment = UnregisteredComment(
        int(request.form['post_id']),
        escape(request.form['author_name']),
        escape(request.form['author_email']),
        escape(request.form['message']),
        datetime.date.today(),
    )
    comments_repository.add_comment(comment)
    return "OK"
