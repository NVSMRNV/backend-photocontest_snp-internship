from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views.users import (
    CurrentUserAPIView,
    RegisterUserAPIView,
    RetrieveUpdateDeleteUserAPIView,
)
from api.docs.schema import schema_view


users_api_urlpatterns = [   
    path('users/registration/', RegisterUserAPIView.as_view(), name=''),
    path('users/current/', CurrentUserAPIView.as_view(), name=''),
    path('users/<int:pk>/', RetrieveUpdateDeleteUserAPIView.as_view(), name=''),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

docs_api_urlpatterns = [
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = [
    path('', include(users_api_urlpatterns)),
    path('', include(docs_api_urlpatterns)),
]
