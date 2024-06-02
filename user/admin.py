from django.contrib import admin

from .models import CustomUser, Candidate, Employer, Company

admin.site.register(Employer)
admin.site.register(Candidate)
admin.site.register(CustomUser)
admin.site.register(Company)