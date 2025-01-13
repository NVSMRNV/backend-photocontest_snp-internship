from django import forms
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.posts.models import Post

class RetrievePostService(ServiceWithResult):
    id = forms.IntegerField()
    custom_validations = ['_validate_post_id']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._get_post_by_id()
        return self
    
    def _get_post_by_id(self):
        try:
            return Post.objects.get(id=self.cleaned_data['id'])
        except ObjectDoesNotExist:
            return None

    def _validate_post_id(self):
        if not self._get_post_by_id():
            self.add_error(
                'id',
                NotFound(
                    message=f'Пост c id: {self.cleaned_data['id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
    