from config.celery import app
from models.models import Post


@app.task
def delete_post_on_delay(post_id: int) -> None:
    post = Post.objects.filter(id=post_id, state='ONDELETE').delete()