from django.contrib import admin
from medias.models import Photo, Video


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        # "__str__",
        "pk",
        "__str__",
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "pk",
    )
