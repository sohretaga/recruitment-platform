from django.contrib import admin
from .models import Employer, Candidate, CustomUser

# Register your models here.

admin.site.register(Employer)
admin.site.register(Candidate)
admin.site.register(CustomUser)