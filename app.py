import datetime
import sqlite3

from flask import Flask
from flask import request
from markupsafe import escape

from comments_repository import CommentsRepository
from consts import lorel_ipsum
from domain import Comment, UnregisteredComment

app = Flask(__name__)
connection = sqlite3.Connection("petitapetitio.db")
comments_repository = CommentsRepository(connection, [
    Comment(1, "Tom", "t@tom.io", "Salut !", datetime.date.today()),
    Comment(2, "Serge", "s@serge.io", "Salut c'est Serge !",
            datetime.date.today() + datetime.timedelta(days=1)),
])


@app.route('/comment/<identifier>')
def hello_world(identifier):
    print(identifier)
    # 1. Interroger la DB
    # 2. Je récupère la liste des commentaires
    # 3. Je renvoie le HTML

    comments = comments_repository.comments()

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
        escape(request.form['author_name']),
        escape(request.form['author_email']),
        escape(request.form['message']),
        datetime.date.today(),
    )
    comments_repository.add_comment(comment)
    return "OK"
