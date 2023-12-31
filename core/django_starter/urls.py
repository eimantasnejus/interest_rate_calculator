from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core.calculator.urls import router as calculator_router

urlpatterns = [
    path("", include("core.calculator.urls")),
    path("api/", include((calculator_router.urls, "calculator"), namespace="calculator")),
    path("admin/", admin.site.urls),
    # 3rd party
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("__debug__/", include("debug_toolbar.urls")),
]
