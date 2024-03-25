from django.contrib import admin
from .models import Employer, CustomUser

# Register your models here.

admin.site.register(Employer)
admin.site.register(CustomUser)