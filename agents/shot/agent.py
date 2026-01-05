"""
Shot Agent - Manages shot production, tracking, and task assignment.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta

from shared.base_agent import BaseAgent
from shared.models import AgentRequest, AgentResponse, Shot, Task, Status, Priority


class ShotAgent(BaseAgent):
    """
    Agent responsible for shot production management.

    Capabilities:
    - Shot creation and tracking
    - Task breakdown and assignment
    - Shot status updates
    - Sequence management
    - Frame range management
    """

    def __init__(self, config_path: str = None):
        super().__init__("shot", config_path)
        self.shots = {}  # In production, this would be a database
        self.tasks = {}

    def _define_capabilities(self) -> List[str]:
        """Define shot agent capabilities."""
        return [
            "create_shot",
            "update_shot_status",
            "assign_task",
            "get_shot_tasks",
            "breakdown_shot",
            "list_shots",
            "get_shot_info",
            "update_frame_range",
            "get_sequence_shots",
        ]

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process shot-related requests."""
        action = request.action
        params = request.parameters

        try:
            if action == "create_shot":
                result = self._create_shot(params)
            elif action == "update_shot_status":
                result = self._update_shot_status(params)
            elif action == "assign_task":
                result = self._assign_task(params)
            elif action == "get_shot_tasks":
                result = self._get_shot_tasks(params)
            elif action == "breakdown_shot":
                result = self._breakdown_shot(params)
            elif action == "list_shots":
                result = self._list_shots(params)
            elif action == "get_shot_info":
                result = self._get_shot_info(params)
            elif action == "update_frame_range":
                result = self._update_frame_range(params)
            elif action == "get_sequence_shots":
                result = self._get_sequence_shots(params)
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

    def _create_shot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new shot."""
        sequence = params.get("sequence")
        shot_number = params.get("shot_number")
        frame_start = params.get("frame_start", 1001)
        frame_end = params.get("frame_end", 1100)
        assets = params.get("assets", [])

        shot_id = f"{sequence}_{shot_number}"
        shot_name = f"{sequence} Shot {shot_number}"

        shot = Shot(
            id=shot_id,
            sequence=sequence,
            number=shot_number,
            name=shot_name,
            status=Status.PENDING,
            frame_range=(frame_start, frame_end),
            assets=assets
        )

        self.shots[shot_id] = shot

        self.logger.info(f"Created shot: {shot_id}")

        return {
            "shot_id": shot_id,
            "name": shot_name,
            "frame_range": [frame_start, frame_end],
            "status": shot.status.value
        }

    def _update_shot_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update shot status."""
        shot_id = params.get("shot_id")
        new_status = params.get("status")

        if shot_id not in self.shots:
            raise ValueError(f"Shot not found: {shot_id}")

        shot = self.shots[shot_id]
        old_status = shot.status

        if isinstance(new_status, str):
            new_status = Status[new_status.upper()]

        shot.status = new_status
        shot.updated_at = datetime.now()

        return {
            "shot_id": shot_id,
            "old_status": old_status.value,
            "new_status": new_status.value
        }

    def _assign_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Assign a task to an artist."""
        shot_id = params.get("shot_id")
        task_name = params.get("task_name")
        department = params.get("department")
        assignee = params.get("assignee")
        priority = params.get("priority", "MEDIUM")
        due_date = params.get("due_date")

        if shot_id not in self.shots:
            raise ValueError(f"Shot not found: {shot_id}")

        task_id = f"{shot_id}_{department}_{task_name}"

        if isinstance(priority, str):
            priority = Priority[priority.upper()]

        task = Task(
            id=task_id,
            name=task_name,
            department=department,
            assignee=assignee,
            status=Status.PENDING,
            priority=priority,
            due_date=datetime.fromisoformat(due_date) if due_date else None
        )

        self.tasks[task_id] = task
        self.shots[shot_id].tasks.append(task)

        return {
            "task_id": task_id,
            "shot_id": shot_id,
            "assignee": assignee,
            "status": task.status.value
        }

    def _get_shot_tasks(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all tasks for a shot."""
        shot_id = params.get("shot_id")

        if shot_id not in self.shots:
            raise ValueError(f"Shot not found: {shot_id}")

        shot = self.shots[shot_id]

        return [
            {
                "id": task.id,
                "name": task.name,
                "department": task.department,
                "assignee": task.assignee,
                "status": task.status.value,
                "priority": task.priority.value
            }
            for task in shot.tasks
        ]

    def _breakdown_shot(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Break down a shot into department tasks."""
        shot_id = params.get("shot_id")
        departments = params.get("departments", [
            "layout", "animation", "fx", "lighting", "comp"
        ])

        if shot_id not in self.shots:
            raise ValueError(f"Shot not found: {shot_id}")

        shot = self.shots[shot_id]
        created_tasks = []

        # Standard VFX pipeline breakdown
        for dept in departments:
            task_id = f"{shot_id}_{dept}"

            task = Task(
                id=task_id,
                name=f"{dept.title()} Task",
                department=dept,
                status=Status.PENDING,
                priority=Priority.MEDIUM
            )

            self.tasks[task_id] = task
            shot.tasks.append(task)

            created_tasks.append({
                "task_id": task_id,
                "department": dept,
                "status": task.status.value
            })

        self.logger.info(f"Created {len(created_tasks)} tasks for shot {shot_id}")

        return created_tasks

    def _list_shots(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List all shots, optionally filtered by sequence."""
        sequence = params.get("sequence")

        shots = []
        for shot in self.shots.values():
            if sequence and shot.sequence != sequence:
                continue

            shots.append({
                "id": shot.id,
                "name": shot.name,
                "sequence": shot.sequence,
                "status": shot.status.value,
                "frame_range": list(shot.frame_range),
                "task_count": len(shot.tasks)
            })

        return shots

    def _get_shot_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed shot information."""
        shot_id = params.get("shot_id")

        if shot_id not in self.shots:
            raise ValueError(f"Shot not found: {shot_id}")

        shot = self.shots[shot_id]

        return {
            "id": shot.id,
            "name": shot.name,
            "sequence": shot.sequence,
            "number": shot.number,
            "status": shot.status.value,
            "frame_range": list(shot.frame_range),
            "assets": shot.assets,
            "tasks": [
                {
                    "id": task.id,
                    "name": task.name,
                    "department": task.department,
                    "status": task.status.value
                }
                for task in shot.tasks
            ],
            "created_at": shot.created_at.isoformat(),
            "updated_at": shot.updated_at.isoformat()
        }

    def _update_frame_range(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update shot frame range."""
        shot_id = params.get("shot_id")
        frame_start = params.get("frame_start")
        frame_end = params.get("frame_end")

        if shot_id not in self.shots:
            raise ValueError(f"Shot not found: {shot_id}")

        shot = self.shots[shot_id]
        old_range = shot.frame_range
        shot.frame_range = (frame_start, frame_end)
        shot.updated_at = datetime.now()

        return {
            "shot_id": shot_id,
            "old_range": list(old_range),
            "new_range": [frame_start, frame_end]
        }

    def _get_sequence_shots(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all shots in a sequence."""
        sequence = params.get("sequence")

        return [
            {
                "id": shot.id,
                "number": shot.number,
                "status": shot.status.value,
                "frame_range": list(shot.frame_range)
            }
            for shot in self.shots.values()
            if shot.sequence == sequence
        ]
