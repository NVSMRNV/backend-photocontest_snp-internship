from django import forms
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.comments.models import Comment
from models.models.posts.models import Post


class ListCommentService(ServiceWithResult):
    post_id = forms.IntegerField()

    custom_validations = ['_validate_post_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._comments()
        return self
    
    def _comments(self) -> QuerySet:
        return Comment.objects.filter(post=self.cleaned_data['post_id'])

    def _get_post_by_id(self):
        try:
            return Post.objects.get(id=self.cleaned_data['post_id'])
        except ObjectDoesNotExist:
            return None

    def _validate_post_id(self):
        if not self._get_post_by_id():
            self.add_error(
                'id',
                NotFound(
                    message=f'Пост c id: {self.cleaned_data['post_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
    