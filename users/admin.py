from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',)
    list_display_links=('id', 'name', 'email',)
    search_fields=('name','email',)
    list_per_page = 25

admin.site.register(User,UserAdmin)
