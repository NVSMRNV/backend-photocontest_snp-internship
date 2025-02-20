from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ForbiddenError
from service_objects.fields import ModelField

from models.models.posts.models import Post
from models.models.users.models import User
from models.models.votes.models import Vote


class ListVoteService(ServiceWithResult):
    post_id = forms.IntegerField()
    
    custom_validations = [
        '_validate_post_exists',
    ]

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._posts()
        return self
    
    def _posts(self) -> QuerySet:
        return Vote.objects.filter(post=self.cleaned_data['post_id'])
    
    def _post(self) -> Post:
        try:
            return Post.objects.get(id=self.cleaned_data['post_id'])
        except ObjectDoesNotExist:
            return None

    def _validate_post_exists(self) -> None:
        if not self._post():
            self.add_error(
                'post_id',
                NotFound(
                    message=f'Пост c id: {self.cleaned_data['post_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
            