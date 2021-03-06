from django.contrib import admin
from .models import *


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()
admin.site.register(Posts, PostAdmin);