from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Photocontest API",
      description='Документация к API по проекту стажировки "Photocontest".',
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)