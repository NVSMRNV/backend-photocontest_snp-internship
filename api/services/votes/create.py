from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import ForbiddenError, NotFound
from service_objects.services import ServiceWithResult

from models.models.posts.models import Post
from models.models.votes.models import Vote


class CreateVoteService(ServiceWithResult):
    user_id = forms.IntegerField(min_value=1)
    post_id = forms.IntegerField(min_value=1)
    
    custom_validations = [
        '_validate_post_exists',
        '_validate_vote_not_exists',
    ]

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._create_vote()
        return self
    
    def _create_vote(self) -> Vote:
        return Vote.objects.create(**self.cleaned_data)
    
    @property
    @lru_cache
    def _post(self) -> Post | None:
        return Post.objects.filter(id=self.cleaned_data['post_id']).first()

    @property
    @lru_cache
    def _vote(self) -> Vote | None:
        return Vote.objects.filter(
            user=self.cleaned_data['user_id'], 
            post=self.cleaned_data['post_id']
        ).first()

    def _validate_post_exists(self) -> None:
        if not self._post:
            self.add_error(
                field='post_id',
                error=NotFound(
                    message=f'Пост c id = {self.cleaned_data['post_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND

    def _validate_vote_not_exists(self) -> None:
        if self._vote():
            self.add_error(
                field='id',
                error=ForbiddenError(
                    message=f'Голос уже существует.'
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST
