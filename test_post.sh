curl -X POST http://127.0.0.1:5000/comment \
    -F author_name="Tom" \
    -F author_email="t@tom.io" \
    -F message="Super le post sf !" \
    -F post_id=sf

curl -X POST http://127.0.0.1:5000/comment \
    -F author_name="Tom" \
    -F author_email="t@tom.io" \
    -F message="Le dbz est bien aussi !" \
    -F post_slug=dbz