from django.contrib import admin

from models.models.posts.models import Post
from models.models.users.models import User


admin.site.register(Post)
admin.site.register(User)


