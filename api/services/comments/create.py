from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from models.models.comments.models import Comment
from models.models.posts.models import Post
from models.models.users.models import User


class CreateCommentService(ServiceWithResult):
    author_id = forms.IntegerField(min_value=1)
    post_id = forms.IntegerField(min_value=1)
    parent_id = forms.IntegerField(min_value=1, required=False)
    text = forms.CharField(max_length=255)
    
    custom_validations = [
        '_validate_post_exists',
        '_validate_parent_exists',
    ]

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()
        
        if self.is_valid():
            self.result = self._create_comment()
        return self
    
    def _create_comment(self):
        return Comment.objects.create(**self.cleaned_data)

    @property
    @lru_cache
    def _post(self) -> Post | None:
        return Post.objects.filter(id=self.cleaned_data['post_id']).first()

    @property
    @lru_cache
    def _parent(self) -> Comment | None:
        if 'parent_id' in self.cleaned_data and self.cleaned_data['parent_id']:
            return Comment.objects.filter(id=self.cleaned_data['parent_id']).first()
        return None

    def _validate_post_exists(self) -> None:
        if not self._post:
            self.add_error(
                field='post_id',
                error=ValidationError(
                    message=f'Пост с id = {self.cleaned_data['author_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND

    def _validate_parent_exists(self) -> None:
        if not self._parent:
            self.add_error(
                field='parent_id',
                error=ValidationError(
                    message=f'Родительский комментарий с id = {self.cleaned_data["parent_id"]} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
