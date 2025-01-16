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
    title = forms.CharField(max_length=127)
    description = forms.CharField(max_length=512)
    image = forms.ImageField()

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self) -> Post:
        return Post.objects.create(
            **self.cleaned_data
        )
