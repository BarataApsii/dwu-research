from django.contrib import admin

from .models import Application, ApplicationDocument


class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'program', 'status', 'email', 'submitted_at')
    list_filter = ('program', 'status')
    search_fields = ('first_name', 'surname', 'full_name', 'email', 'research_topic')
    inlines = [ApplicationDocumentInline]
