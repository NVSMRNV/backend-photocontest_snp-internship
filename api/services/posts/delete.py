from functools import lru_cache
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from api.tasks import delete_post_on_delay
from models.models.posts.models import Post


class DeletePostService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    
    custom_validations = ['_validate_post_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            delete_post_on_delay.apply_async(args=(self._post,), countdown=7)
            self.response_status = status.HTTP_204_NO_CONTENT 
        return self

    @property
    @lru_cache
    def _post(self) -> Post | None:
        return Post.objects.filter(id=self.cleaned_data['id']).first()

    def _validate_post_id(self) -> None:
        if not self._post:
            self.add_error(
                field='id',
                error=NotFound(
                    message=f'Пост c id = {self.cleaned_data['id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
