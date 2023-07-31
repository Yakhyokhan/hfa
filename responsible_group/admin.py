from django.contrib import admin
from .models import ResponsibleGroup, ResponsiblePerson, Filler

# Register your models here.

admin.site.register(ResponsibleGroup)
admin.site.register(ResponsiblePerson)
admin.site.register(Filler)