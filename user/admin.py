from django.contrib import admin

from .models import CustomUser, Candidate, Employer

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'username', 'user_type']

    def get_full_name(self, obj):
        if obj.user_type == 'employer':
            return obj.first_name
        else:
            return f'{obj.first_name} {obj.last_name}'

    get_full_name.short_description = 'Full Name'

admin.site.register(Employer)
admin.site.register(Candidate)