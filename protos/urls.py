
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api_schema/", get_schema_view(title="Protos API Endpoints",
                                        description="The endpoints for API services",
                                        version=1.0), name="api_schema"),
    path("api_docs/", TemplateView.as_view(template_name="api_endpoints.html",
                                           extra_context={
                                               "schema_url": "api_schema"
                                           })),

    path("location/", include("location.urls")),
    path("account/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
