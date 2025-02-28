from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from models.models.comments.models import Comment
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound


class UpdatePatchCommentService(ServiceWithResult):
    comment_id = forms.IntegerField()
    text = forms.CharField()

    custom_validations = ['_validate_comment']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.comment = self._comment()
            self.result = self._update_comment()
        return self

    def _comment(self):
        try:
            return Comment.objects.get(id=self.cleaned_data['comment_id'])
        except ObjectDoesNotExist:
            return None


    def _update_comment(self):
        self.comment.text = self.cleaned_data.get('text', self.comment.text)
        self.comment.save()

        return self.comment


    def _validate_comment(self):
        if not self._comment():
            self.add_error(
                'id',
                NotFound(
                    message=f'Комментарий с id={self.cleaned_data['comment_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND


class UpdatePutCommentService():
    comment_id = forms.IntegerField()

    custom_validations = ['_validate_comment']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.comment = self._comment()
            self.result = self._update_comment()
        return self

    def _comment(self):
        try:
            return Comment.objects.get(id=self.cleaned_data['comment_id'])
        except ObjectDoesNotExist:
            return None


    def _update_comment(self):
        self.comment.text = self.cleaned_data.get('text', '')
        self.comment.save()

        return self.comment


    def _validate_comment(self):
        if not self._comment():
            self.add_error(
                'id',
                NotFound(
                    message=f'Комментарий с id={self.cleaned_data['comment_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND