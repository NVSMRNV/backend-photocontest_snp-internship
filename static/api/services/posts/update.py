from functools import lru_cache
from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.posts.models import Post


class UpdatePostService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    title = forms.CharField(max_length=127, required=False)
    description = forms.CharField(max_length=511, required=False)
    image = forms.ImageField(required=False)

    custom_validations = ['_validate_post_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._update_post()
        return self

    @property
    @lru_cache
    def _post(self) -> Post | None:
        return Post.objects.filter(id=self.cleaned_data['id']).first()

    def _update_post(self) -> Post:
        pass

    def _validate_post_id(self) -> None:
        if not self._post:
            self.add_error(
                field='id',
                error=NotFound(
                    message=f'Пост c id = {self.cleaned_data['id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND


class PartialUpdatePostService(UpdatePostService):
    def _update_post(self) -> Post:
        for field in ['title', 'description', 'image']:
            value = self.cleaned_data.get(field)
            if value:
                setattr(self._post, field, value)
        self._post.save()
        return self._post


class FullUpdatePostService(UpdatePostService):
    def _update_post(self) -> Post:
        for field in ['title', 'description', 'image']:
            value = self.cleaned_data.get(field)
            if value:
                setattr(self._post, field, value)
            else:
                setattr(self._post, field, None)
        self._post.save()
        return self._post