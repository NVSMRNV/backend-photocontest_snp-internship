from config.celery import app
from models.models import Post


@app.task
def delete_post_on_delay(post: Post) -> None:
    post.delete()