from functools import lru_cache
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError

from models.models.comments.models import Comment
from models.models.posts.models import Post
from models.models.users.models import User


class CreateCommentService(ServiceWithResult):
    author_id = forms.IntegerField()
    post_id = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    text = forms.CharField()
    
    custom_validations = [
        '_validate_author_exists',
        '_validate_post_exists',
        '_validate_parent_exists',
    ]

    def process(self):
        self.run_custom_validations()
        
        if self.is_valid():
            self.result = self._create_comment()
        return self
    
    def _create_comment(self):
        return Comment.objects.create(
            **self.cleaned_data
        )

    @lru_cache
    def _author(self):
        try:
            return User.objects.get(id=self.cleaned_data['author_id'])
        except ObjectDoesNotExist():
            return None

    @lru_cache
    def _post(self):
        try:
            return Post.objects.get(id=self.cleaned_data['post_id'])
        except ObjectDoesNotExist():
            return None

    @lru_cache
    def _parent(self):
        if 'parent_id' in self.cleaned_data and self.cleaned_data['parent_id']:
            try:
                return Comment.objects.get(id=self.cleaned_data['parent_id'])
            except Comment.DoesNotExist:
                return None
        return None

    def _validate_author_exists(self):
        if not self._author:
            self.add_error(
                'author_id',
                ValidationError(
                    message=f'Пользователь с id={self.cleaned_data['author_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST

    def _validate_post_exists(self):
        if not self._post:
            self.add_error(
                'post_id',
                ValidationError(
                    message=f'Пост с id={self.cleaned_data['author_id']} не найден.'
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST



    def _validate_parent_exists(self):
        if 'parent_id' in self.cleaned_data and self.cleaned_data['parent_id']:
            if not self._parent():
                self.add_error(
                    'parent_id',
                    ValidationError(
                        message=f'Родительский комментарий с id={self.cleaned_data["parent_id"]} не найден.'
                    )
                )
                self.response_status = status.HTTP_400_BAD_REQUEST
    
