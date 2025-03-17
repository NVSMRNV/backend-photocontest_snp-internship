from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.comments.models import Comment


class UpdateCommentService(ServiceWithResult):
    comment_id = forms.IntegerField(min_value=1)
    text = forms.CharField(max_length=255, required=False)

    custom_validations = ['_validate_comment_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._update_comment()
        return self

    @property
    @lru_cache
    def _comment(self) -> Comment | None:
        return Comment.objects.filter(id=self.cleaned_data['comment_id']).first()

    def _update_comment(self) -> Comment:
        pass

    def _validate_comment_id(self) -> None:
        if not self._comment:
            self.add_error(
                field='comment_id',
                error=NotFound(
                    message=f'Комментарий с id = {self.cleaned_data['comment_id']} не найден.'
                )
            )
            self.response_status=status.HTTP_404_NOT_FOUND


class PartialUpdateCommentService(UpdateCommentService):
    def _update_comment(self) -> Comment:
        text = self.cleaned_data.get('text')
        if text:
            setattr(self._comment, 'text', text)
        self._comment.save()
        return self._comment


class FullUpdateCommentService(UpdateCommentService):
    def _update_comment(self) -> Comment:
        text = self.cleaned_data.get('text')
        if text:
            setattr(self._comment, 'text', text)
        else:
            setattr(self._comment, 'text', None)
        self._comment.save()
        return self._comment
