from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from api.docs.schema import schema_view
from api.views.comments import (
    ListCreateCommentAPIView,
    RetrieveUpdateDeleteCommentAPIView
)
from api.views.posts import (
    ListCreatePostAPIView,
    RetrieveUpdateDeletePostAPIView
    )
from api.views.users import (
    CurrentUserAPIView,
    RegisterUserAPIView,
    RetrieveUpdateDeleteUserAPIView
)
from api.views.votes import CreateDeleteVoteAPIView

#! COMMENTS
comments_api_urlpatterns = [
    path('comments/', ListCreateCommentAPIView.as_view()),
    path('comments/<int:id>/', RetrieveUpdateDeleteCommentAPIView.as_view()),
]

#! VOTES
votes_api_urlpatterns = [
    path('votes/', CreateDeleteVoteAPIView.as_view(),),
]

#! POSTS
posts_api_urlpatterns = [
    path('posts/', ListCreatePostAPIView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', RetrieveUpdateDeletePostAPIView.as_view(), name='post_retrieve_update_delete'),
]

#! USERS
users_api_urlpatterns = [   
    path('users/current/', CurrentUserAPIView.as_view()),
    path('users/registration/', RegisterUserAPIView.as_view()),
    path('users/<int:id>/', RetrieveUpdateDeleteUserAPIView.as_view()),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

#! DOCS
docs_api_urlpatterns = [
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = [
    path('', include(posts_api_urlpatterns)),
    path('', include(comments_api_urlpatterns)),
    path('', include(votes_api_urlpatterns)),
    path('', include(users_api_urlpatterns)),
    path('', include(docs_api_urlpatterns)),
]
