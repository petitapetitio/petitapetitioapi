curl -X POST http://127.0.0.1:5000/comment \
    -F author_name="Tom" \
    -F author_email="t@tom.io" \
    -F message="Super le post 1 !" \
    -F post_id=1

curl -X POST http://127.0.0.1:5000/comment \
    -F author_name="Tom" \
    -F author_email="t@tom.io" \
    -F message="Le 2 est bien aussi !" \
    -F post_id=2