from django import forms
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from models.models.posts.models import Post
from models.models.users.models import User


class CreatePostService(ServiceWithResult):
    author = ModelField(User)
    title = forms.CharField()
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self) -> Post:
        return Post.objects.create(
            **self.cleaned_data
        )
