from django.contrib import admin
from .models import Ticket

# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'requester_name', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'requester__first_name', 'requester__last_name', 'requester__email')
    readonly_fields = ('created_at', 'updated_at', 'requester')

    def save_model(self, request, obj, form, change):
        if not change or not obj.requester_id:
            obj.requester = request.user
        super().save_model(request, obj, form, change)