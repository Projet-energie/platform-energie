hooks:
    build: |
        pip install -r requirements.txt
        pip install -e .
        pip install gunicorn 