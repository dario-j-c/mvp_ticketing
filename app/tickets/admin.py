from django.contrib import admin

from tickets.models import (
    Attachment,
    BugReport,
    FeatureRequest,
    Project,
    Task,
    Technology,
    TechnologyCategory,
    Ticket,
)


class AuditAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(AuditAdmin):
    list_display = [
        "name",
        "project_lead",
        "total_tickets",
        "completed_tickets",
        "completion_percentage",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "project_lead", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = AuditAdmin.readonly_fields + (
        "total_tickets",
        "completed_tickets",
        "completion_percentage",
    )
    filter_horizontal = ["members"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project_lead")


@admin.register(TechnologyCategory)
class TechnologyCategoryAdmin(AuditAdmin):
    list_display = ["name", "description", "technology_count"]
    search_fields = ["name", "description"]

    def technology_count(self, obj):
        return obj.technologies.count()

    technology_count.short_description = "Technologies"


@admin.register(Technology)
class TechnologyAdmin(AuditAdmin):
    list_display = ["name", "category", "version", "usage_count", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]
    readonly_fields = AuditAdmin.readonly_fields + ("usage_count",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")


@admin.register(Ticket)
class TicketAdmin(AuditAdmin):
    list_display = [
        "ticket_id",
        "title",
        "project",
        "status",
        "priority",
        "ticket_type",
        "owner",
        "reporter_name",
        "technology_display",
        "created_at",
    ]
    list_filter = [
        "status",
        "priority",
        "ticket_type",
        "project",
        "owner",
        "technologies__category",
        "created_at",
    ]
    search_fields = ["ticket_id", "title", "reporter_name", "description"]
    readonly_fields = AuditAdmin.readonly_fields + ("ticket_id", "technology_summary")
    filter_horizontal = ["technologies", "assigned_users"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("ticket_id", "title", "description", "ticket_type")},
        ),
        ("Project & Technology", {"fields": ("project", "technologies")}),
        (
            "Status & Assignment",
            {"fields": ("status", "priority", "owner", "assigned_users")},
        ),
        (
            "Reporter Information",
            {
                "fields": (
                    "reporter",
                    "reporter_name",
                    "reporter_contact",
                    "reporter_department",
                )
            },
        ),
        (
            "Business Context",
            {"fields": ("business_impact",), "classes": ("collapse",)},
        ),
        (
            "Summary",
            {
                "fields": ("technology_summary",),
                "classes": ("collapse",),
                "description": "Auto-generated summary of selected technologies",
            },
        ),
        (
            "Audit",
            {
                "fields": ("created_at", "modified_at", "created_by", "modified_by"),
                "classes": ("collapse",),
            },
        ),
    )

    def technology_display(self, obj):
        """Display first few technologies in list view"""
        techs = obj.technologies.all()[:3]
        tech_names = [tech.name for tech in techs]
        if obj.technologies.count() > 3:
            tech_names.append(f"+ {obj.technologies.count() - 3} more")
        return ", ".join(tech_names) if tech_names else "None"

    technology_display.short_description = "Technologies"

    def save_model(self, request, obj, form, change):
        # Auto-assign if S.E. user is creating/editing
        if not change and request.user.is_se_team and not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("project", "owner")
            .prefetch_related("technologies", "assigned_users")
        )


# Inline admins for ticket details
class BugReportInline(admin.StackedInline):
    model = BugReport
    extra = 0
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


class FeatureRequestInline(admin.StackedInline):
    model = FeatureRequest
    extra = 0
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    readonly_fields = ("created_at", "modified_at", "created_by", "modified_by")


# Add inlines to TicketAdmin
TicketAdmin.inlines = [
    BugReportInline,
    FeatureRequestInline,
    TaskInline,
    AttachmentInline,
]


# Custom admin actions for bulk operations
@admin.action(description="Export selected tickets with technology details")
def export_tickets_with_tech(modeladmin, request, queryset):
    """Custom export that includes technology information"""
    import csv

    from django.http import HttpResponse

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tickets_with_tech.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Ticket ID",
            "Title",
            "Project",
            "Status",
            "Priority",
            "Owner",
            "Assigned Users",
            "Technologies",
            "Technology Categories",
        ]
    )

    for ticket in queryset.prefetch_related("technologies__category", "assigned_users"):
        tech_names = ", ".join([tech.name for tech in ticket.technologies.all()])
        tech_categories = ", ".join(
            list(set([tech.category.name for tech in ticket.technologies.all()]))
        )
        assigned_users = ", ".join(
            [user.username for user in ticket.assigned_users.all()]
        )

        writer.writerow(
            [
                ticket.ticket_id,
                ticket.title,
                ticket.project.name,
                ticket.status,
                ticket.priority,
                ticket.owner.username if ticket.owner else "",
                assigned_users,
                tech_names,
                tech_categories,
            ]
        )

    return response


TicketAdmin.actions = [export_tickets_with_tech]
