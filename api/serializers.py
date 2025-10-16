from rest_framework import serializers
from django.db.models import Count
from .models import Organization, User, File, Download


class FileSerializer(serializers.ModelSerializer):
    download_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = File
        fields = ["id", "file", "uploaded_by", "organization", "uploaded_at", "download_count"]
        read_only_fields = ["uploaded_by", "organization", "uploaded_at", "download_count"]


class OrganizationSerializer(serializers.ModelSerializer):
    total_downloads = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "total_downloads"]


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ["id", "file", "user", "organization", "downloaded_at"]
        read_only_fields = ["user", "organization", "downloaded_at"]
