from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from models.models.comments.models import Comment
from models.models.posts.models import Post
from models.models.users.models import User
from models.models.votes.models import Vote
from utils.flows import Flow

from viewflow.fsm import TransitionNotAllowed


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = (
        'state',
    )
    search_fields = (
        'title',
    )
    fields = [
        'id',
        'title',
        'author',
        'image_thumbnail',
        'image',
        'state',
        'votes_number',
        'comments_number',
    ]
    list_display = (
        'id',
        'image_thumbnail',
        'title',
        'author',
        'state',
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
    readonly_fields = (
        'id',
        'votes_number',
        'comments_number',
        'image_thumbnail',
    )

    def image_thumbnail(self, post: Post):
        url = f"/admin/{post._meta.app_label}/{post._meta.model_name}/{post.id}/change/"
        return mark_safe(f'<a href="{url}"><img src="{post.image_thumbnail.url}" width="150" height="150" /></a>')
    image_thumbnail.short_description = 'Фото'

    def reject_posts(self, request, queryset):
        for post in queryset:
            flow = Flow(post)
            try:
                flow.reject()
                post.save()
            except TransitionNotAllowed:
                self.message_user(request, 'Ошибка: Один или несколько постов нельзя отклонить.', messages.ERROR)
                return
        self.message_user(request, 'Выбранные посты успешно отклонены.', messages.SUCCESS)
    reject_posts.short_description = 'Отклонить выбранные посты'

    def approve_posts(self, request, queryset):
        for post in queryset:
            flow = Flow(post)
            try:
                flow.approve()
                post.save()
            except TransitionNotAllowed:
                self.message_user(request, 'Ошибка: Один или несколько постов нельзя одобрить.', messages.ERROR)
                return
        self.message_user(request, 'Выбранные посты успешно одобрены.', messages.SUCCESS)
    approve_posts.short_description = 'Одобрить выбранные посты'

    def pending_posts(self, request, queryset):
        for post in queryset:
            flow = Flow(post)
            try:
                flow.pending()
                post.save()
            except TransitionNotAllowed:
                self.message_user(request, 'Ошибка: Один или несколько постов нельзя отправить на модерацию.', messages.ERROR)
                return
        self.message_user(request, 'Выбранные посты успешно отправлены на модерацию.', messages.SUCCESS)
            
    pending_posts.short_description = 'На модерацию выбранные посты'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...
