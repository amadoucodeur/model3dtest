from django.contrib import admin
from .models import Badge, CustomUser, Model3d

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Badge)
admin.site.register(Model3d)

