from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import NotFound, ValidationError
from service_objects.services import ServiceWithResult

from models.models.comments.models import Comment


class DeleteCommentService(ServiceWithResult):
    comment_id = forms.IntegerField(min_value=1)
    
    custom_validations = ['_validate_comment_id', '_validate_no_child_comments']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self._comment.delete()
            self.response_status = status.HTTP_200_OK 
        return self
    
    @property
    @lru_cache
    def _comment(self) -> Comment | None:
        return Comment.objects.filter(id=self.cleaned_data['comment_id']).first()

    def _validate_comment_id(self) -> None:
        if not self._comment:
            self.add_error(
                field='comment_id',
                error=NotFound(
                    message=f'Комментарий с id = {self.cleaned_data['comment_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
    
    def _validate_no_child_comments(self) -> None:
        if self._comment and self._comment.replies.exists():
            self.add_error(
                field='comment_id',
                error=ValidationError(
                    message=(
                        f'Комментарий с id = {self.cleaned_data["comment_id"]}' 
                        'имеет дочерние комментарии и не может быть удален.'
                    )
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST
