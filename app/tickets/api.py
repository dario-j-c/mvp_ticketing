from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from tickets.models import Project, Technology, TechnologyCategory, Ticket

api = NinjaAPI(title="SE Ticketing API", version="0.1")
User = get_user_model()


# Enhanced schemas for MVP
class TechnologyOut(Schema):
    id: int
    name: str
    category: str
    usage_count: int


class ProjectOut(Schema):
    id: int
    name: str
    total_tickets: int
    completed_tickets: int
    completion_percentage: float
    members: List[str]


class TicketOut(Schema):
    id: int
    ticket_id: str
    title: str
    status: str
    priority: str
    ticket_type: str
    project: str
    technologies: List[str]
    reporter_name: str
    owner: Optional[str] = None
    assigned_users: List[str]
    created_at: str


class TicketCreateSchema(Schema):
    title: str
    description: str
    ticket_type: str
    project_id: int
    technology_ids: List[int] = []
    reporter_name: str
    reporter_contact: str
    priority: str = "medium"


@api.get("/tickets/", response=List[TicketOut])
def list_tickets(
    request, status: Optional[str] = None, project_id: Optional[int] = None
):
    """List tickets with optional filters"""
    tickets = Ticket.objects.select_related("project", "owner").prefetch_related(
        "technologies", "assigned_users"
    )

    if status:
        tickets = tickets.filter(status=status)
    if project_id:
        tickets = tickets.filter(project_id=project_id)

    return [
        {
            "id": t.id,
            "ticket_id": t.ticket_id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "ticket_type": t.ticket_type,
            "project": t.project.name,
            "technologies": [tech.name for tech in t.technologies.all()],
            "reporter_name": t.reporter_name,
            "owner": t.owner.username if t.owner else None,
            "assigned_users": [user.username for user in t.assigned_users.all()],
            "created_at": t.created_at.isoformat(),
        }
        for t in tickets
    ]


@api.get("/projects/", response=List[ProjectOut])
def list_projects(request):
    """List all projects with ticket statistics"""
    projects = Project.objects.prefetch_related("members").all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "total_tickets": p.total_tickets,
            "completed_tickets": p.completed_tickets,
            "completion_percentage": p.completion_percentage,
            "members": [member.username for member in p.members.all()],
        }
        for p in projects
    ]


@api.get("/technologies/", response=List[TechnologyOut])
def list_technologies(request, category: Optional[str] = None):
    """List technologies with usage statistics"""
    technologies = Technology.objects.select_related("category").annotate(
        ticket_count=Count("tickets")
    )

    if category:
        technologies = technologies.filter(category__name=category)

    return [
        {
            "id": t.id,
            "name": t.name,
            "category": t.category.name,
            "usage_count": t.ticket_count,
        }
        for t in technologies
    ]


# REPORTING ENDPOINTS - I assume key for motivating usage!


@api.get("/reports/individual/{username}/")
def get_individual_report(request, username: str):
    """Individual S.E. member report - THIS IS KEY"""
    try:
        user = User.objects.get(username=username, is_se_team=True)
    except User.DoesNotExist:
        return {"error": "User not found or not S.E. team member"}

    tickets = (
        Ticket.objects.filter(Q(owner=user) | Q(assigned_users=user))
        .distinct()
        .prefetch_related("technologies__category", "project")
    )

    # Technology analysis
    tech_usage = {}
    tech_categories = {}
    project_work = {}

    for ticket in tickets:
        # Track project work
        project_name = ticket.project.name
        if project_name not in project_work:
            project_work[project_name] = {"total": 0, "completed": 0}
        project_work[project_name]["total"] += 1
        if ticket.status == "completed":
            project_work[project_name]["completed"] += 1

        # Track technology usage
        for tech in ticket.technologies.all():
            tech_name = tech.name
            category = tech.category.name

            if tech_name not in tech_usage:
                tech_usage[tech_name] = 0
            tech_usage[tech_name] += 1

            if category not in tech_categories:
                tech_categories[category] = 0
            tech_categories[category] += 1

    return {
        "user": user.get_full_name() or user.username,
        "summary": {
            "total_tickets": tickets.count(),
            "completed": tickets.filter(status="completed").count(),
            "in_progress": tickets.filter(status="in_progress").count(),
            "completion_rate": round(
                (tickets.filter(status="completed").count() / tickets.count() * 100), 1
            )
            if tickets.count() > 0
            else 0,
        },
        "technology_expertise": {
            "most_used_technologies": dict(
                sorted(tech_usage.items(), key=lambda x: x[1], reverse=True)[:10]
            ),
            "technology_categories": tech_categories,
            "total_technologies_used": len(tech_usage),
        },
        "project_contributions": project_work,
        "recent_work": [
            {
                "ticket_id": t.ticket_id,
                "title": t.title,
                "project": t.project.name,
                "status": t.status,
                "technologies": [tech.name for tech in t.technologies.all()],
            }
            for t in tickets.order_by("-modified_at")[:10]
        ],
    }


@api.get("/reports/team-technology/")
def get_team_technology_report(request):
    """Team-wide technology usage report"""

    # Get all S.E. team members
    se_users = User.objects.filter(is_se_team=True)

    # Technology usage across team
    tech_stats = (
        Technology.objects.annotate(
            ticket_count=Count("tickets"),
            user_count=Count(
                "tickets__assigned_users",
                distinct=True,
                filter=Q(tickets__assigned_users__is_se_team=True),
            ),
        )
        .select_related("category")
        .order_by("-ticket_count")
    )

    # Category usage
    category_stats = TechnologyCategory.objects.annotate(
        ticket_count=Count("technologies__tickets"),
        user_count=Count(
            "technologies__tickets__assigned_users",
            distinct=True,
            filter=Q(technologies__tickets__assigned_users__is_se_team=True),
        ),
    ).order_by("-ticket_count")

    return {
        "team_size": se_users.count(),
        "technology_diversity": {
            "total_technologies_used": tech_stats.filter(ticket_count__gt=0).count(),
            "most_popular_technologies": [
                {
                    "name": tech.name,
                    "category": tech.category.name,
                    "tickets": tech.ticket_count,
                    "team_members_using": tech.user_count,
                }
                for tech in tech_stats[:15]
            ],
            "category_breakdown": [
                {
                    "category": cat.name,
                    "tickets": cat.ticket_count,
                    "team_members_using": cat.user_count,
                }
                for cat in category_stats
            ],
        },
    }


@api.get("/reports/project/{project_id}/")
def get_project_report(request, project_id: int):
    """Detailed project report with technology analysis"""
    project = get_object_or_404(Project, id=project_id)
    tickets = project.tickets.prefetch_related(
        "technologies__category", "owner", "assigned_users"
    )

    # Technology usage in this project
    tech_usage = {}
    contributors = set()

    for ticket in tickets:
        if ticket.owner:
            contributors.add(ticket.owner.username)
        for user in ticket.assigned_users.all():
            contributors.add(user.username)
        for tech in ticket.technologies.all():
            if tech.name not in tech_usage:
                tech_usage[tech.name] = 0
            tech_usage[tech.name] += 1

    return {
        "project": {
            "name": project.name,
            "description": project.description,
            "completion_percentage": project.completion_percentage,
        },
        "progress": {
            "total_tickets": project.total_tickets,
            "completed": project.completed_tickets,
            "in_progress": tickets.filter(status="in_progress").count(),
            "staging": tickets.filter(status="staging").count(),
        },
        "technology_stack": dict(
            sorted(tech_usage.items(), key=lambda x: x[1], reverse=True)
        ),
        "contributors": list(contributors),
        "recent_activity": [
            {
                "ticket_id": t.ticket_id,
                "title": t.title,
                "status": t.status,
                "owner": t.owner.username if t.owner else None,
                "updated": t.modified_at.isoformat(),
            }
            for t in tickets.order_by("-modified_at")[:10]
        ],
    }
