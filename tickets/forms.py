"""Form definitions for the tickets app."""

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class BulkAssignForm(forms.Form):
    """Collect a target user for bulk ticket assignment.

    This form is used by the Django admin bulk action that reassigns
    multiple selected tickets to one user.

    Attributes:
        assigned_to (forms.ModelChoiceField): User dropdown populated from
                                              the active user model.
    """

    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Assign to User",
        empty_label="-- Select a User --",
    )