from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Listen)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Premium)
