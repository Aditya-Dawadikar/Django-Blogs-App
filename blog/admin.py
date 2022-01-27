from django.contrib import admin

# Register your models here.
from blog.models import User,Blog

admin.site.register(User)
admin.site.register(Blog)