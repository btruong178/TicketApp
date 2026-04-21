"""
Django admin configuration for the "tickets" application

Includes:

    Classes:
    - TicketAdmin: For the "Ticket" model
    - TicketNoteAdmin: For the "TicketNote" model
    - TicketNoteInline: Inline admin for "TicketNote" within "Ticket"

    Functions:
    - bulk_resolve_tickets: Action to mark selected tickets as resolved
    - bulk_assign_tickets: Action to assign selected tickets to a user

"""
from django.contrib import admin
from django.shortcuts import render, redirect
from .forms import BulkAssignForm
from .models import Ticket, TicketNote
from unfold.admin import ModelAdmin


class TicketNoteInline(admin.TabularInline):
    """Inline admin for TicketNote within Ticket.

    Displays existing notes and allows adding new notes directly from the Ticket detail page.

    """
    model = TicketNote
    extra = 1
    readonly_fields = ('author', 'created_at', 'updated_at')


def bulk_resolve_tickets(modeladmin, request, queryset):
    """Mark all selected tickets as resolved.

    Bulk action that updates "status" to "resolved" for all selected tickets

    Args:
        modeladmin (ModelAdmin): The TicketAdmin instance calling this action.
        request (HttpRequest): HTTP request from the admin user.
        queryset (QuerySet): A queryset of selected Ticket objects to resolve.

    Returns:
        None: Updates the queryset

    """
    queryset.update(status='resolved')

bulk_resolve_tickets.short_description = "Resolve selected Support Tickets"


def bulk_assign_tickets(modeladmin, request, queryset):
    """Assign selected tickets to a chosen user via a form.

    A two-step bulk action:
        1. First POST (From - changelist): 
           Renders a form showing
           selected tickets and a user dropdown.
        2. Second POST (From - form):
           Validates the form, updates all selected tickets
           with the chosen user, and redirects back to the
           changelist with a success message.
    
    Args:
        modeladmin (ModelAdmin): The TicketAdmin instance calling this action.
        request (HttpRequest): The current HTTP request.
        queryset (QuerySet): A queryset of selected Ticket from changelist.

    Returns:
        HttpResponse: Rendered assign form
        HttpResponseRedirect: Redirects back to changelist

    """
    if 'apply' in request.POST:
        form = BulkAssignForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['assigned_to']
            selected_ids = request.POST.getlist('_selected_action')
            Ticket.objects.filter(pk__in=selected_ids).update(assigned_to=user)
            target_label = (user.get_full_name() or user.username) if user else '-'
            modeladmin.message_user(
                request,
                f"{len(selected_ids)} ticket(s) assigned to {target_label}."
            )
            return redirect(request.get_full_path().split('?')[0])
    else:
        form = BulkAssignForm()

    return render(request, 'admin/bulk_assign.html', {
        'form': form,
        'tickets': queryset,
        'selected_ids': queryset.values_list('pk', flat=True),
        **modeladmin.admin_site.each_context(request),
    })

bulk_assign_tickets.short_description = "Assign selected Support Tickets"


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    """Admin configuration for the Ticket model.
    
    Attributes:
        list_display (tuple): Fields to display in the changelist view.
        list_filter (tuple): Fields to filter by in the changelist sidebar.
        search_fields (tuple): Fields to include in the search functionality.
        readonly_fields (tuple): Fields that are read-only in the admin form.
        inlines (list): Inline admin classes to include in the Ticket detail view.
        actions (list): Custom actions available in the changelist view.
    
    Methods:
        save_model: Overrides to set requester on ticket creation.
        save_formset: Overrides to set author on new inline TicketNotes.
    """
    list_display = ('title', 'status', 'priority', 'requester_name', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'requester__first_name', 'requester__last_name', 'requester__email')
    readonly_fields = ('created_at', 'updated_at', 'requester')
    inlines = [TicketNoteInline]
    actions = [bulk_resolve_tickets, bulk_assign_tickets]

    def save_model(self, request, obj, form, change):
        """Set requester to current user when creating a new ticket.

        Overrides ModelAdmin.save_model to auto-assign the logged-in
        user as the requester on ticket creation only, not on edits.

        Args:
            request (HttpRequest): The current request containing the logged-in user.
            obj (Ticket): The Ticket instance being saved.
            form (ModelForm): The submitted form instance.
            change (bool): True if editing existing ticket, False if creating new.

        Returns:
            None: Delegates final save to super().save_model().
        """
        if not change or not obj.requester_id:
            obj.requester = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Set author to current user when creating new inline TicketNotes.

        Overrides ModelAdmin.save_formset to auto-assign the logged-in
        user as the author on TicketNote creation only, not on edits.

        Args:
            request (HttpRequest): The current request containing the logged-in user.
            form (ModelForm): The parent Ticket form.
            formset (BaseInlineFormSet): The inline formset containing TicketNote instances.
            change (bool): True if editing existing ticket, False if creating new.

        Returns:
            None: Saves all instances, handles deletions
        """
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TicketNote) and not instance.author_id:
                instance.author = request.user
            instance.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()


@admin.register(TicketNote)
class TicketNoteAdmin(ModelAdmin):
    """Admin configuration for the TicketNote model.

    Provides a standalone admin view for ticket notes
    
    Attributes:
        list_display (tuple): Fields to display in the changelist view.
        readonly_fields (tuple): Fields that are read-only in the admin form.
        search_fields (tuple): Fields to include in the search functionality.
    """
    list_display = ('ticket', 'note_title', 'author', 'created_at', 'updated_at')
    list_filter = ('author',)
    readonly_fields = ('created_at', 'updated_at', 'author')
    search_fields = ('ticket__title', 'author__username')

    def save_model(self, request, obj, form, change):
        """Set author to current user when creating a new ticket note.

        Overrides ModelAdmin.save_model to auto-assign the logged-in
        user as the author on note creation only, not on edits.

        Args:
            request (HttpRequest): The current request containing the logged-in user.
            obj (TicketNote): The TicketNote instance being saved.
            form (ModelForm): The submitted form instance.
            change (bool): True if editing existing note, False if creating new.

        Returns:
            None: Delegates final save to super().save_model().
        """
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


