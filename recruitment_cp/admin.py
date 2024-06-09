from django.contrib import admin
from .models import Language, SiteContent
# Register your models here.

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_default', 'is_active']

    def save_model(self, request, obj, form, change):
        if obj.is_default:
            Language.objects.exclude(pk = obj.pk).update(is_default=False)
        super().save_model(request, obj, form, change)

class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['page', 'content', 'image']

admin.site.register(Language, LanguageAdmin)
admin.site.register(SiteContent, SiteContentAdmin)