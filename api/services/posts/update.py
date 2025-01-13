from django import forms
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound

from models.models.posts.models import Post


class UpdatePatchPostService(ServiceWithResult):
    id = forms.IntegerField()
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    custom_validations = ['_validate_post_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.post = self._get_post_by_id()
            self.post = self._update_post()
        return self
    
    def _update_post(self) -> Post:
        self.cleaned_data = self._clear_cleaned_data()
        self.post.title = self.cleaned_data.get('title', self.post.title)
        self.post.description = self.cleaned_data.get('description', self.post.description)
        self.post.image = self.cleaned_data.get('image', self.post.image)
        self.post.save()

        return self.post

    def _clear_cleaned_data(self) -> dict:
        result = {}
        for key, value in self.cleaned_data.items():
            if value:
               result[key] = value 
        return result

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


class UpdatePutPostService(ServiceWithResult):
    id = forms.IntegerField()
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    custom_validations = ['_validate_post_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.post = self._get_post_by_id()
            self.post = self._update_post()
        return self
    
    def _update_post(self) -> Post:
        self.cleaned_data = self._clear_cleaned_data()
        self.post.title = self.cleaned_data.get('title')
        self.post.description = self.cleaned_data.get('description')
        self.post.image = self.cleaned_data.get('image')
        self.post.save()

        return self.post

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
