from django.contrib import admin
from .models import Contact, ContactEmail

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'date']

@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ['email']