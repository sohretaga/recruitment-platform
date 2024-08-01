from django.contrib import admin
from .models import Contact, ContactEmail, Subscribe, HowItWork, Team

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
    list_display = ['title']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'profession']