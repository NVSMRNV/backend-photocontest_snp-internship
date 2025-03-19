from functools import lru_cache
from django import forms

from django.db import models
from django.db.models import BooleanField, QuerySet, Exists, OuterRef, Value
from service_objects.services import ServiceWithResult

from models.models.posts.models import Post
from models.models.users.models import User
from models.models.votes.models import Vote


class ListPostService(ServiceWithResult):
    user_id = forms.IntegerField(min_value=1, required=False)
    author_id = forms.IntegerField(min_value=1, required=False)

    def process(self) -> ServiceWithResult:
        self.result = self._posts
        return self
    
    @property
    @lru_cache
    def _user(self) -> User | None:
        return User.objects.filter(id=self.cleaned_data['user_id']).first()


    @property
    def _posts(self) -> QuerySet:
        if self.cleaned_data.get('author_id'):
            return Post.objects.filter(author_id=self.cleaned_data['author_id']).annotate(
                is_liked_by_user=Exists(
                    Vote.objects.filter(post=OuterRef('pk'), user_id=self._user)
                )
            )
        elif self._user:
            return Post.objects.all().annotate(
                is_liked_by_user=Exists(
                    Vote.objects.filter(post=OuterRef('pk'), user_id=self._user)
                )
            )
        else:
            return Post.objects.all().annotate(
                is_liked_by_user=Value(False, output_field=BooleanField())
            )