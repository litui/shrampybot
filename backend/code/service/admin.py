from django.contrib import admin

# Register your models here.
from service.models import Service, UserService

class ServiceAdmin(admin.ModelAdmin):
    pass

class UserServiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Service, ServiceAdmin)
admin.site.register(UserService, UserServiceAdmin)