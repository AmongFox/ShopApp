from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfileModel


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfileModel
    list_display = ('user', 'name', 'surname')
    search_fields = ('user__username',)


admin.site.register(UserProfileModel, UserProfileAdmin)
