from django.contrib import admin
from .models import Project, Chapter, ProjectVersion, Asset

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'book_type', 'created_at', 'updated_at')
    list_filter = ('book_type', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'author__username')
    date_hierarchy = 'created_at'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'order', 'created_at', 'updated_at')
    list_filter = ('project', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('project', 'order')

@admin.register(ProjectVersion)
class ProjectVersionAdmin(admin.ModelAdmin):
    list_display = ('project', 'version_number', 'created_at', 'created_by')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title', 'comment')
    date_hierarchy = 'created_at'

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'asset_type', 'created_at')
    list_filter = ('asset_type', 'created_at')
    search_fields = ('title', 'description', 'project__title')
