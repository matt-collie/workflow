"""
Production Agent - Manages production tracking, scheduling, and reporting.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta

from shared.base_agent import BaseAgent
from shared.models import AgentRequest, AgentResponse, Status


class ProductionAgent(BaseAgent):
    """
    Agent responsible for production management and coordination.

    Capabilities:
    - Production tracking and reporting
    - Schedule management
    - Resource allocation
    - Milestone tracking
    - Deliverable management
    """

    def __init__(self, config_path: str = None):
        super().__init__("production", config_path)
        self.projects = {}
        self.milestones = {}
        self.deliverables = {}

    def _define_capabilities(self) -> List[str]:
        """Define production agent capabilities."""
        return [
            "track_progress",
            "generate_report",
            "update_milestone",
            "allocate_resources",
            "track_deliverable",
            "get_project_status",
            "calculate_burndown",
            "forecast_completion",
        ]

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process production-related requests."""
        action = request.action
        params = request.parameters

        try:
            if action == "track_progress":
                result = self._track_progress(params)
            elif action == "generate_report":
                result = self._generate_report(params)
            elif action == "update_milestone":
                result = self._update_milestone(params)
            elif action == "allocate_resources":
                result = self._allocate_resources(params)
            elif action == "track_deliverable":
                result = self._track_deliverable(params)
            elif action == "get_project_status":
                result = self._get_project_status(params)
            elif action == "calculate_burndown":
                result = self._calculate_burndown(params)
            elif action == "forecast_completion":
                result = self._forecast_completion(params)
            else:
                return AgentResponse(
                    request_id=request.id,
                    success=False,
                    data=None,
                    message=f"Unknown action: {action}"
                )

            return AgentResponse(
                request_id=request.id,
                success=True,
                data=result,
                message=f"Successfully executed {action}"
            )

        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return AgentResponse(
                request_id=request.id,
                success=False,
                data=None,
                message=str(e)
            )

    def _track_progress(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Track production progress."""
        project_id = params.get("project_id")
        date = params.get("date", datetime.now().date().isoformat())

        # In production, this would query actual project data
        progress = {
            "project_id": project_id,
            "date": date,
            "total_shots": 150,
            "completed_shots": 45,
            "in_progress_shots": 38,
            "pending_shots": 67,
            "completion_percentage": 30.0,
            "on_schedule": True
        }

        return progress

    def _generate_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate production report."""
        project_id = params.get("project_id")
        report_type = params.get("report_type", "weekly")  # daily, weekly, monthly
        start_date = params.get("start_date")
        end_date = params.get("end_date")

        # In production, this would aggregate actual data
        report = {
            "project_id": project_id,
            "report_type": report_type,
            "period": {
                "start": start_date,
                "end": end_date
            },
            "summary": {
                "shots_completed": 12,
                "assets_published": 5,
                "reviews_held": 3,
                "render_hours": 2847
            },
            "by_department": {
                "layout": {"completed": 15, "in_progress": 8},
                "animation": {"completed": 12, "in_progress": 10},
                "lighting": {"completed": 8, "in_progress": 12},
                "comp": {"completed": 10, "in_progress": 6}
            },
            "generated_at": datetime.now().isoformat()
        }

        self.logger.info(f"Generated {report_type} report for {project_id}")

        return report

    def _update_milestone(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update project milestone."""
        milestone_id = params.get("milestone_id")
        status = params.get("status")
        completion_date = params.get("completion_date")

        milestone = {
            "id": milestone_id,
            "status": status,
            "completion_date": completion_date,
            "updated_at": datetime.now().isoformat()
        }

        self.milestones[milestone_id] = milestone

        self.logger.info(f"Updated milestone {milestone_id} to {status}")

        return milestone

    def _allocate_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate resources to tasks."""
        project_id = params.get("project_id")
        department = params.get("department")
        resource_count = params.get("resource_count")
        duration_weeks = params.get("duration_weeks")

        allocation = {
            "project_id": project_id,
            "department": department,
            "resource_count": resource_count,
            "duration_weeks": duration_weeks,
            "start_date": datetime.now().date().isoformat(),
            "end_date": (datetime.now() + timedelta(weeks=duration_weeks)).date().isoformat(),
            "allocated_at": datetime.now().isoformat()
        }

        self.logger.info(f"Allocated {resource_count} {department} resources for {duration_weeks} weeks")

        return allocation

    def _track_deliverable(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Track project deliverable."""
        deliverable_id = params.get("deliverable_id")
        name = params.get("name")
        due_date = params.get("due_date")
        status = params.get("status", "pending")

        deliverable = {
            "id": deliverable_id,
            "name": name,
            "due_date": due_date,
            "status": status,
            "created_at": datetime.now().isoformat()
        }

        self.deliverables[deliverable_id] = deliverable

        self.logger.info(f"Tracking deliverable: {name}")

        return deliverable

    def _get_project_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive project status."""
        project_id = params.get("project_id")

        # In production, this would query actual project data
        status = {
            "project_id": project_id,
            "name": "Project Alpha",
            "status": "in_progress",
            "start_date": "2025-01-01",
            "end_date": "2025-06-30",
            "progress": {
                "overall": 35.0,
                "asset_creation": 65.0,
                "shot_production": 28.0,
                "post_production": 5.0
            },
            "team_size": 45,
            "budget_used": 62.5,
            "milestones": {
                "completed": 3,
                "upcoming": 2,
                "total": 8
            },
            "deliverables": {
                "completed": 2,
                "pending": 4,
                "overdue": 0
            },
            "health": "on_track"
        }

        return status

    def _calculate_burndown(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate burndown chart data."""
        project_id = params.get("project_id")
        days = params.get("days", 30)

        # In production, this would calculate from actual task completion data
        burndown_data = []
        total_tasks = 500
        ideal_rate = total_tasks / days

        for day in range(days):
            # Simulate burndown with some variance
            completed = int(ideal_rate * day * (0.9 + 0.2 * (day % 3) / 3))
            ideal = int(ideal_rate * day)

            burndown_data.append({
                "day": day,
                "completed": completed,
                "ideal": ideal,
                "remaining": total_tasks - completed
            })

        return {
            "project_id": project_id,
            "total_tasks": total_tasks,
            "burndown": burndown_data
        }

    def _forecast_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Forecast project completion date."""
        project_id = params.get("project_id")

        # In production, this would use actual velocity data
        forecast = {
            "project_id": project_id,
            "current_progress": 35.0,
            "average_velocity": 2.5,  # % per week
            "estimated_completion": (datetime.now() + timedelta(weeks=26)).date().isoformat(),
            "scheduled_completion": "2025-06-30",
            "variance_days": 7,
            "confidence": "high",
            "risks": [
                "Render capacity during peak weeks",
                "Asset approval delays"
            ],
            "recommendations": [
                "Add 2 additional lighting artists for weeks 15-20",
                "Expedite asset review process"
            ]
        }

        return forecast
