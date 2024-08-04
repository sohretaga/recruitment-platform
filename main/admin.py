from django.contrib import admin
from .models import Contact, ContactEmail, Subscribe, HowItWork, Team, Service

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'date']

@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribe_date']

@admin.register(HowItWork)
class HowItWorkAdmin(admin.ModelAdmin):
    list_display = ['title_with_no']

    def title_with_no(self, obj):
        return f'{obj.no}.{obj.title}'

    title_with_no.short_description = 'Title'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'profession']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_description']

    def short_description(self, obj):
        return f'{obj.description[:75]}...' if len(obj.description) > 75 else obj.description
    
    short_description.short_description = 'Description'