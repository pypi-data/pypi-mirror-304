from django.contrib import admin
from .models import Model1


class Model1Admin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Model1, Model1Admin)
