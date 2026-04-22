from .models import Ticket


def dashboard_callback(request, context):
    """Inject ticket summary statistics into the admin dashboard context.

    Called by Unfold before rendering the admin index page.
    Adds a 'summary' dict and a 'recent_tickets' queryset to the template context.

    Args:
        request (HttpRequest): The current HTTP request.
        context (dict): The existing template context from Unfold.

    Returns:
        dict: The updated context.
    """
    tickets = Ticket.objects.all()

    context["summary"] = {
        "total": tickets.count(),
        "new": tickets.filter(status="new").count(),
        "in_progress": tickets.filter(status="in_progress").count(),
        "resolved": tickets.filter(status="resolved").count(),
        "unassigned": tickets.filter(assigned_to__isnull=True).count(),
        "high_priority": tickets.filter(priority=3).count(),
    }

    context["recent_tickets"] = (
        tickets
        .select_related("requester", "assigned_to")
        .order_by("-created_at")[:5]
    )

    return context
