from django.contrib import admin
from .models import *

# Register your models here.




class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "created_at")
admin.site.register(User, UserAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_by")
admin.site.register(Ticket, TicketAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("poster", "created_at")
admin.site.register(Comment, CommentAdmin)