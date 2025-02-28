from django import forms
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.comments.models import Comment


class DeleteCommentService(ServiceWithResult):
    comment_id = forms.IntegerField()
    custom_validations = ['_validate_comment_id']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.comment = self._get_comment_by_id()
            self.comment.delete()
            self.response_status = status.HTTP_204_NO_CONTENT 
        return self
    
    def _get_comment_by_id(self):
        try:
            return Comment.objects.get(id=self.cleaned_data['comment_id'])
        except ObjectDoesNotExist:
            return None

    def _validate_comment_id(self):
        if not self._get_comment_by_id():
            self.add_error(
                'comment_id',
                NotFound(
                    message=f'Комментарий с id: {self.cleaned_data['comment_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND