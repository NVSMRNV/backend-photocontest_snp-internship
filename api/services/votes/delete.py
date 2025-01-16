from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import NotFound

from models.models.posts.models import Post
from models.models.users.models import User
from models.models.votes.models import Vote


class DeleteVoteService(ServiceWithResult):
    user_id = forms.IntegerField()
    post_id = forms.IntegerField()
    
    custom_validations = ['_validate_vote_exists']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.vote = self._vote()
            self.vote.delete()
            self.response_status = status.HTTP_204_NO_CONTENT
        return self
    
    def _vote(self) -> Vote:
        try:
            return Vote.objects.get(
                user=self.cleaned_data['user_id'],
                post=self.cleaned_data['post_id']
            )
        except ObjectDoesNotExist:
            return None
        
    def _validate_vote_exists(self):
        if not self._vote():
            self.add_error(
                'id',
                NotFound(
                    message=f'Лайк от пользователя: {self.cleaned_data['user_id']} к посту {self.cleaned_data['post_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
