from django.contrib import admin

from .models import CustomUser, Candidate, Employer

admin.site.register(Employer)
admin.site.register(Candidate)
admin.site.register(CustomUser)