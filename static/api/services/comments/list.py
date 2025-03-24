from django import forms
from django.db.models import QuerySet
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.comments.models import Comment
from models.models.posts.models import Post


class ListCommentService(ServiceWithResult):
    post_id = forms.IntegerField(min_value=1)

    custom_validations = ['_validate_post_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._comments()
        return self
    
    def _comments(self) -> QuerySet:
        return Comment.objects.filter(post=self.cleaned_data['post_id'])

    def _post(self) -> Post | None:
        return Post.objects.filter(id=self.cleaned_data['post_id']).first()

    def _validate_post_id(self):
        if not self._post():
            self.add_error(
                field='post_id',
                error=NotFound(
                    message=f'Пост c id = {self.cleaned_data['post_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
    