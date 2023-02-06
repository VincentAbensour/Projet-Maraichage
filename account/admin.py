from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class AccountAdmin(UserAdmin):
    list_display = ('email','date_joined','last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(models.Account, AccountAdmin)