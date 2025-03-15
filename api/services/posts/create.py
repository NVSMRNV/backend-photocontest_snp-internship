from django import forms

from service_objects.services import ServiceWithResult

from models.models.posts.models import Post


class CreatePostService(ServiceWithResult):
    author = forms.IntegerField(min_value=1)
    title = forms.CharField(max_length=127)
    description = forms.CharField(max_length=511)
    image = forms.ImageField()

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self) -> Post:
        return Post.objects.create(**self.cleaned_data)
