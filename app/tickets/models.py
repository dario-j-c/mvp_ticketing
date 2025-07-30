from django.conf import settings
from django.db import models
from django.utils import timezone


class AuditModel(models.Model):
    """Abstract model for auditing."""

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_modified",
    )

    class Meta:
        abstract = True


class Project(AuditModel):
    """Projects to group tickets for reporting and organization"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # Optional project metadata
    start_date = models.DateField(null=True, blank=True)
    target_completion = models.DateField(null=True, blank=True)
    project_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_projects",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects", blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def total_tickets(self):
        return self.tickets.count()

    @property
    def completed_tickets(self):
        return self.tickets.filter(status="completed").count()

    @property
    def completion_percentage(self):
        total = self.total_tickets
        if total == 0:
            return 0
        return round((self.completed_tickets / total) * 100, 1)


class TechnologyCategory(AuditModel):
    """Categories for organizing technologies"""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7, default="#6c757d", help_text="Hex color for UI display"
    )

    class Meta:
        verbose_name_plural = "Technology Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Technology(AuditModel):
    """Technologies used in tickets - standardized naming"""

    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        TechnologyCategory, on_delete=models.CASCADE, related_name="technologies"
    )
    description = models.TextField(blank=True)
    version = models.CharField(
        max_length=50, blank=True, help_text="Current version if relevant"
    )
    documentation_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def usage_count(self):
        """How many tickets use this technology"""
        return self.tickets.count()


class Ticket(AuditModel):
    """Main ticket model - simpler MVP approach"""

    STATUS_CHOICES = [
        ("staging", "Staging"),
        ("accepted", "Accepted/Validated"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
        ("frozen", "Frozen"),
    ]

    PRIORITY_CHOICES = [
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    TICKET_TYPE_CHOICES = [
        ("bug", "Bug Report"),
        ("feature", "Feature Request"),
        ("task", "Task"),
    ]

    # Basic Information
    ticket_id = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)

    # Project and Technology Tracking
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tickets"
    )
    technologies = models.ManyToManyField(
        Technology,
        blank=True,
        related_name="tickets",
        help_text="Technologies used/involved in this ticket",
    )

    # Status & Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="staging")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )

    # People
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_tickets",
    )
    reporter_name = models.CharField(max_length=100)  # Always filled
    reporter_contact = models.CharField(max_length=100)
    reporter_department = models.CharField(max_length=100, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_tickets",
        help_text="The primary owner of the ticket",
    )
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tickets", blank=True
    )

    # Business Context
    business_impact = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)

    def generate_ticket_id(self):
        """Generate SE-2025-001 format IDs"""
        year = timezone.now().year
        prefix = f"SE-{year}-"
        last_ticket = (
            Ticket.objects.filter(ticket_id__startswith=prefix)
            .order_by("-ticket_id")
            .first()
        )

        if last_ticket:
            last_num = int(last_ticket.ticket_id.split("-")[-1])
            new_num = last_num + 1
        else:
            new_num = 1

        return f"{prefix}{new_num:03d}"

    def __str__(self):
        return f"{self.ticket_id}: {self.title}"

    @property
    def technology_summary(self):
        """Get comma-separated list of technologies for display"""
        return ", ".join([tech.name for tech in self.technologies.all()])

    @property
    def technology_by_category(self):
        """Get technologies grouped by category for reporting"""
        tech_dict = {}
        for tech in self.technologies.select_related("category").all():
            category = tech.category.name
            if category not in tech_dict:
                tech_dict[category] = []
            tech_dict[category].append(tech.name)
        return tech_dict


# Specific ticket type details using OneToOne (cleaner for MVP)
class BugReport(AuditModel):
    """Bug-specific details"""

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, primary_key=True)

    CATEGORY_CHOICES = [
        ("error_page", "Error Page"),
        ("unexpected_behavior", "Unexpected Behaviour"),
        ("perceived_lag", "Perceived Lag"),
        ("data_issue", "Data Issue"),
        ("access_issue", "Access Issue"),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    url_location = models.URLField(blank=True)
    browser_device = models.CharField(max_length=100, blank=True)
    steps_to_reproduce = models.TextField()
    expected_results = models.TextField()
    actual_results = models.TextField()

    def __str__(self):
        return f"Bug: {self.ticket.title}"


class FeatureRequest(AuditModel):
    """Feature-specific details"""

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, primary_key=True)

    CATEGORY_CHOICES = [
        ("aesthetic", "Aesthetic"),
        ("functionality", "Functionality"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    current_situation = models.TextField()
    desired_functionality = models.TextField()
    success_criteria = models.TextField()
    business_value = models.TextField()

    def __str__(self):
        return f"Feature: {self.ticket.title}"


class Task(AuditModel):
    """Task-specific details"""

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, primary_key=True)

    TASK_TYPE_CHOICES = [
        ("data_update", "Data Update"),
        ("configuration", "Configuration"),
        ("documentation", "Documentation"),
        ("maintenance", "Maintenance"),
        ("research", "Research"),
    ]

    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    detailed_description = models.TextField()
    acceptance_criteria = models.TextField()

    def __str__(self):
        return f"Task: {self.ticket.title}"


# Simple attachments support
class Attachment(AuditModel):
    """File attachments for tickets"""

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="attachments/%Y/%m/")
    original_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ticket.ticket_id}: {self.original_name}"
