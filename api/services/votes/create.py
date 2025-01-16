from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ForbiddenError
from service_objects.fields import ModelField

from models.models.posts.models import Post
from models.models.users.models import User
from models.models.votes.models import Vote


class CreateVoteService(ServiceWithResult):
    user_id = forms.IntegerField()
    post_id = forms.IntegerField()
    
    custom_validations = [
        '_validate_post_exists',
        '_validate_vote_not_exists',
    ]

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._create_vote()
        return self
    
    def _create_vote(self) -> Vote:
        return Vote.objects.create(
            **self.cleaned_data
        )
    
    def _post(self) -> Post:
        try:
            return Post.objects.get(id=self.cleaned_data['post_id'])
        except ObjectDoesNotExist:
            return None
    
    def _vote(self) -> Vote:
        try:
            return Vote.objects.get(
                user=self.cleaned_data['user_id'],
                post=self.cleaned_data['post_id']
            )
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

    def _validate_vote_not_exists(self) -> None:
        if self._vote():
            self.add_error(
                'id',
                ForbiddenError(
                    message=f'Голос уже существует.'
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST

