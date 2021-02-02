from django.contrib import admin
from .models import Schedule, BotServer, AuthorizeClient

# Register your models here.
admin.site.register(Schedule)
admin.site.register(BotServer)
admin.site.register(AuthorizeClient)