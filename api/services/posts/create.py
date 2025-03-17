from django import forms

from service_objects.services import ServiceWithResult

from models.models.posts.models import Post
from models.models.users.models import User


class CreatePostService(ServiceWithResult):
    author_id = forms.IntegerField(min_value=1)
    title = forms.CharField(max_length=127)
    description = forms.CharField(max_length=511)
    image = forms.ImageField()

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self) -> Post:
        return Post.objects.create(author=self._author, **self.cleaned_data)

    @property
    def _author(self):
        return User.objects.get(id=self.cleaned_data['author_id'])
