from django.contrib import admin
from .models import properties,Client,Inquiry,Interaction,Appointment,Contract

# Register your models here.

class propertyyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'agent',)
    list_display_links=('id','agent','title','slug',)
    list_filter=('agent',)
    search_fields=('title','description',)
    list_per_page = 25

admin.site.register(properties,propertyyAdmin)
admin.site.register(Client)
admin.site.register(Inquiry)
admin.site.register(Interaction)
admin.site.register(Appointment)
admin.site.register(Contract)

