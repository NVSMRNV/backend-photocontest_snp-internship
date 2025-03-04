from django.contrib import admin
from django.utils.safestring import mark_safe
from django_fsm import TransitionNotAllowed

from models.models.posts.models import Post
from models.models.users.models import User
from models.models.comments.models import Comment
from models.models.votes.models import Vote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = (
        'status',
    )
    search_fields = (
        'title',
    )
    list_display = (
        'id',
        'image_thumbnail',
        'title',
        'author',
        'status',
        'votes_number',
        'comments_number',
    )
    ordering = (
        '-created',
    )
    actions = [
        'reject_posts',
        'approve_posts',
        'pending_posts',
    ]

    def image_thumbnail(self, post: Post):
        return mark_safe(f'<img src="{post.image_thumbnail.url}" width="50" height="50" />')
    image_thumbnail.short_description = 'Фото'

    def reject_posts(self, request, queryset):
        for post in queryset:
            try:
                post.to_state_rej()
                post.save()
            except TransitionNotAllowed:
                return
    reject_posts.short_description = 'Отклонить выбранные посты'

    def approve_posts(self, request, queryset):
        for post in queryset:
            try:
                post.to_state_app()
                post.save()
            except TransitionNotAllowed:
                return
    approve_posts.short_description = 'Одобрить выбранные посты'

    def pending_posts(self, request, queryset):
        for post in queryset:
            try:
                post.to_state_pen()
                post.save()
            except TransitionNotAllowed:
                return
    pending_posts.short_description = 'На модерацию выбранные посты'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...
