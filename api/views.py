from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.db.models import Count
from .models import File, Download, Organization, User
from .serializers import FileSerializer, DownloadSerializer, OrganizationSerializer


# 1. Upload + list files
# 2. Users can see ALL files across orgs
class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Annotate each file with download count
        return File.objects.all().annotate(download_count=Count("downloads"))

    def perform_create(self, serializer):
        serializer.save(
            uploaded_by=self.request.user,
            organization=self.request.user.organization,
        )

    # 2. Download endpoint (records download)
    @action(detail=True, methods=["get"], url_path="download")
    def download_file(self, request, pk=None):
        file = self.get_object()
        Download.objects.create(
            user=request.user,
            organization=request.user.organization,
            file=file,
        )
        return FileResponse(file.file.open("rb"), as_attachment=True)


# 4. Organizations + total downloads
class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all().annotate(total_downloads=Count("files__downloads"))


# 3. Downloads
class DownloadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DownloadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Download.objects.all()

    # 5. Downloads by a single user
    @action(detail=False, methods=["get"], url_path="by-user/(?P<user_id>[^/.]+)")
    def downloads_by_user(self, request, user_id=None):
        qs = Download.objects.filter(user__id=user_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # 6. Downloads for a single file
    @action(detail=False, methods=["get"], url_path="by-file/(?P<file_id>[^/.]+)")
    def downloads_by_file(self, request, file_id=None):
        qs = Download.objects.filter(file__id=file_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
