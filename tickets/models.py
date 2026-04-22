"""
Data models for the tickets application.

Includes:

    Classes:
    - Ticket: Represents a support ticket submitted by a user
    - TicketNote: Represents a note attached to a support ticket
    
"""
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    """Support ticket submitted by a user.

    Tracks the lifecycle of a support request from creation
    through resolution, including priority, status, requester,
    and the assignee responsible for handling the ticket.

    Attributes:

        STATUS_CHOICES (list[tuple]): Valid status values for a ticket.
        PRIORITY_CHOICES (list[tuple]): Valid priority levels (1-3).

        title (CharField): Short summary of the issue.
        description (TextField): Full description of the issue.
        status (CharField): Current lifecycle state of the ticket.
        priority (IntegerField): Urgency level of the ticket.
        requester (ForeignKey): The user who submitted the ticket.
        assigned_to (ForeignKey): The user assigned to resolve the ticket.
        created_at (DateTimeField): Timestamp when the ticket was created.
        updated_at (DateTimeField): Timestamp when the ticket was last modified.

    Methods:
        requester_name: Returns the full name of the requester or username if full name is not set.
        requester_email: Returns the email address of the requester or 'N/A' if not set.
        __str__: Returns the ticket title as the string representation.

    """

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        (3, 'High'),
        (2, 'Medium'),
        (1, 'Low'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requested_tickets'
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'

    def requester_name(self):
        """Return the name of user

        Returns:
            str: Full name if set, otherwise the username.
        """
        return self.requester.get_full_name() or self.requester.username

    def requester_email(self):
        """Return the email address of the requester.

        Returns:
            str: Email address if set, otherwise 'N/A'.
        """
        return self.requester.email or 'N/A'

    def __str__(self):
        """Return the ticket title as the string representation.

        Returns:
            str: The title of the ticket.
        """
        return self.title


class TicketNote(models.Model):
    """Note attached to a support ticket.

    Notes are authored by users and tied to a specific ticket.

    Attributes:
        ticket (ForeignKey): The ticket this note belongs to.
        author (ForeignKey): The user who wrote the note.
        notes (TextField): The full content of the note.
        created_at (DateTimeField): Timestamp when the note was created.
        updated_at (DateTimeField): Timestamp when the note was last modified.
    """

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Ticket Note'
        verbose_name_plural = 'Ticket Notes'

    def note_title(self):
        """Return a truncated preview of the note content.

        Truncates the note to 10 characters and appends '...'
        if the content exceeds 10 characters.

        Returns:
            str: First 10 characters followed by '...' if truncated,
                otherwise the full note content.

        Example:
            >>> note.notes = "This is a long note"
            >>> note.note_title()
            "This is a ..."

            >>> note.notes = "ShortNote"
            >>> note.note_title()
            "ShortNote"
        """
        if len(self.notes) > 10:
            return self.notes[:10] + "..."
        return self.notes

    def __str__(self):
        """Return a string representation identifying the note author.

        Returns:
            str: Author's username followed by "'s Note".

        Example:
            >>> str(note)
            "brian's Note"
        """
        return f"{self.author.username}'s Note"