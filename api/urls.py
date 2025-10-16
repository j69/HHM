from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, DownloadViewSet, OrganizationViewSet

router = DefaultRouter()
router.register("files", FileViewSet, basename="file")
router.register("downloads", DownloadViewSet, basename="download")
router.register("organizations", OrganizationViewSet, basename="organization")

urlpatterns = [
    path("", include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]