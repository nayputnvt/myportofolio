from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project

# serializer buat model project 
class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    # alias project_image_url mengarah ke field thumbnail biar kompatibel
    project_image_url = serializers.URLField(source="thumbnail", required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "category", "tech_stack",
            "project_url", "thumbnail", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    # validasi judul: gak boleh kosong dan bersihin tag html
    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    # bersihin deskripsi dari tag html
    def validate_description(self, value):
        return strip_tags(value)

    # bersihin tech stack dari tag html
    def validate_tech_stack(self, value):
        return strip_tags(value)

    # hitung total star yang didapat project
    def get_star_count(self, obj):
        return obj.starred_by.count()

    # cek apakah user yang login lagi nge star project ini
    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    # gabungin username yang ngasih star jadi string
    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


# serializer buat model experience
class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "started_at", "is_ongoing"]

    # validasi judul: gak boleh kosong dan bersihin tag html
    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    # bersihin deskripsi dari tag html
    def validate_description(self, value):
        return strip_tags(value)

    # hitung total star yang didapat experience
    def get_star_count(self, obj):
        return obj.starred_by.count()

    # cek apakah user yang login lagi nge-star experience ini
    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    # gabungin username yang ngasih star jadi string
    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
