# Admin registration for the portfolio app.
#
# Register models here so they can be viewed and managed via
# the Django admin interface (/admin).

from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, Project, Service


# ──────────────────────────────────────────────
#  Projects
# ──────────────────────────────────────────────

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'image_preview',
        'title',
        'category',
        'badge',
        'featured',
        'updated_at',
    )
    list_display_links = ('title',)
    list_editable = ('order', 'featured')
    list_filter = ('category', 'featured', 'category_slug')
    search_fields = ('title', 'description', 'tags', 'badge')
    readonly_fields = ('image_preview_large', 'created_at', 'updated_at')
    ordering = ('order',)

    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'description', 'url'),
        }),
        ('Image', {
            'fields': ('image', 'image_url', 'image_preview_large'),
            'description': 'Upload an image <strong>or</strong> paste an external URL. '
                           'Uploaded images take priority.',
        }),
        ('Categorisation & Tags', {
            'fields': ('category', 'category_slug', 'badge', 'tags', 'featured'),
        }),
        ('Ordering & Dates', {
            'fields': ('order', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Preview')
    def image_preview(self, obj):
        url = obj.display_image
        if url:
            return format_html(
                '<img src="{}" style="width:60px; height:40px; object-fit:cover; '
                'border-radius:4px; border:1px solid #333;" />',
                url,
            )
        return '—'

    @admin.display(description='Image Preview')
    def image_preview_large(self, obj):
        url = obj.display_image
        if url:
            return format_html(
                '<img src="{}" style="max-width:400px; max-height:250px; '
                'border-radius:8px; border:1px solid #555;" />',
                url,
            )
        return 'No image set.'


# ──────────────────────────────────────────────
#  Services
# ──────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'image_preview',
        'title',
        'category',
        'badge',
        'updated_at',
    )
    list_display_links = ('title',)
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title', 'description', 'tags', 'badge')
    readonly_fields = ('image_preview_large', 'created_at', 'updated_at')
    ordering = ('order',)

    fieldsets = (
        ('Service Details', {
            'fields': ('title', 'category', 'description'),
        }),
        ('Image', {
            'fields': ('image', 'image_url', 'image_preview_large'),
            'description': 'Upload an image <strong>or</strong> paste an external URL. '
                           'Uploaded images take priority.',
        }),
        ('Deliverables & Tags', {
            'fields': ('deliverables', 'tags', 'badge'),
            'description': 'Enter one deliverable per line. Tags are comma-separated.',
        }),
        ('Ordering & Dates', {
            'fields': ('order', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Preview')
    def image_preview(self, obj):
        url = obj.display_image
        if url:
            return format_html(
                '<img src="{}" style="width:60px; height:40px; object-fit:cover; '
                'border-radius:4px; border:1px solid #333;" />',
                url,
            )
        return '—'

    @admin.display(description='Image Preview')
    def image_preview_large(self, obj):
        url = obj.display_image
        if url:
            return format_html(
                '<img src="{}" style="max-width:400px; max-height:250px; '
                'border-radius:8px; border:1px solid #555;" />',
                url,
            )
        return 'No image set.'


# ──────────────────────────────────────────────
#  Contact Messages
# ──────────────────────────────────────────────

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
