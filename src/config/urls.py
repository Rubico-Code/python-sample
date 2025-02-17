from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # type: ignore
from drf_spectacular.utils import extend_schema, extend_schema_view # type: ignore


def redirect_root(request):
    return redirect("swagger-ui", permanent=True)



urlpatterns = [
    path("", redirect_root),  # Redirect root to /redoc
    # path("console/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/', include([
    
    path("auth/", include("djoser.urls")),
    path("users/", include("users.urls")),
    path("profiles/", include("profiles.urls")),
    
    ])),
]


admin.site.site_header = "rubico Admin"
admin.site.site_title = "rubico Admin Portal"
admin.site.index_title = "Welcome to rubico Admin Portal"
