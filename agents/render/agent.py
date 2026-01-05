"""
Render Agent - Manages render farm operations and job scheduling.
"""
from typing import List, Dict, Any
from datetime import datetime

from shared.base_agent import BaseAgent
from shared.models import AgentRequest, AgentResponse, RenderJob, Status, Priority


class RenderAgent(BaseAgent):
    """
    Agent responsible for render farm management.

    Capabilities:
    - Render job submission
    - Job monitoring and status updates
    - Priority management
    - Error detection and retry
    - Resource allocation
    """

    def __init__(self, config_path: str = None):
        super().__init__("render", config_path)
        self.render_jobs = {}  # In production, this would interface with Deadline/Tractor
        self.farm_capacity = self.config.get("farm_capacity", 100)

    def _define_capabilities(self) -> List[str]:
        """Define render agent capabilities."""
        return [
            "submit_job",
            "get_job_status",
            "update_job_priority",
            "cancel_job",
            "retry_failed_frames",
            "list_jobs",
            "get_farm_status",
            "monitor_job",
        ]

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process render-related requests."""
        action = request.action
        params = request.parameters

        try:
            if action == "submit_job":
                result = self._submit_job(params)
            elif action == "get_job_status":
                result = self._get_job_status(params)
            elif action == "update_job_priority":
                result = self._update_job_priority(params)
            elif action == "cancel_job":
                result = self._cancel_job(params)
            elif action == "retry_failed_frames":
                result = self._retry_failed_frames(params)
            elif action == "list_jobs":
                result = self._list_jobs(params)
            elif action == "get_farm_status":
                result = self._get_farm_status(params)
            elif action == "monitor_job":
                result = self._monitor_job(params)
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

    def _submit_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a render job to the farm."""
        shot_id = params.get("shot_id")
        job_name = params.get("job_name")
        frames = params.get("frames", [])
        render_layer = params.get("render_layer", "beauty")
        output_path = params.get("output_path")
        priority = params.get("priority", "MEDIUM")
        submitted_by = params.get("submitted_by", "system")

        if not frames:
            raise ValueError("No frames specified for render job")

        job_id = f"render_{shot_id}_{render_layer}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if isinstance(priority, str):
            priority = Priority[priority.upper()]

        job = RenderJob(
            id=job_id,
            shot_id=shot_id,
            name=job_name,
            status=Status.PENDING,
            priority=priority,
            frames=frames,
            render_layer=render_layer,
            output_path=output_path,
            submitted_by=submitted_by
        )

        self.render_jobs[job_id] = job

        self.logger.info(f"Submitted render job: {job_id} with {len(frames)} frames")

        return {
            "job_id": job_id,
            "status": job.status.value,
            "frame_count": len(frames),
            "priority": priority.value
        }

    def _get_job_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed status of a render job."""
        job_id = params.get("job_id")

        if job_id not in self.render_jobs:
            raise ValueError(f"Render job not found: {job_id}")

        job = self.render_jobs[job_id]

        total_frames = len(job.frames)
        completed_frames = len(job.completed_frames)
        failed_frames = len(job.failed_frames)
        progress = (completed_frames / total_frames * 100) if total_frames > 0 else 0

        return {
            "job_id": job_id,
            "name": job.name,
            "status": job.status.value,
            "priority": job.priority.value,
            "total_frames": total_frames,
            "completed_frames": completed_frames,
            "failed_frames": failed_frames,
            "progress": round(progress, 2),
            "submitted_at": job.submitted_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None
        }

    def _update_job_priority(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update render job priority."""
        job_id = params.get("job_id")
        new_priority = params.get("priority")

        if job_id not in self.render_jobs:
            raise ValueError(f"Render job not found: {job_id}")

        job = self.render_jobs[job_id]
        old_priority = job.priority

        if isinstance(new_priority, str):
            new_priority = Priority[new_priority.upper()]

        job.priority = new_priority

        self.logger.info(f"Updated job {job_id} priority: {old_priority.name} -> {new_priority.name}")

        return {
            "job_id": job_id,
            "old_priority": old_priority.value,
            "new_priority": new_priority.value
        }

    def _cancel_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel a render job."""
        job_id = params.get("job_id")

        if job_id not in self.render_jobs:
            raise ValueError(f"Render job not found: {job_id}")

        job = self.render_jobs[job_id]
        job.status = Status.CANCELLED
        job.completed_at = datetime.now()

        self.logger.info(f"Cancelled render job: {job_id}")

        return {
            "job_id": job_id,
            "status": job.status.value,
            "cancelled_at": job.completed_at.isoformat()
        }

    def _retry_failed_frames(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retry failed frames for a job."""
        job_id = params.get("job_id")

        if job_id not in self.render_jobs:
            raise ValueError(f"Render job not found: {job_id}")

        job = self.render_jobs[job_id]
        failed_count = len(job.failed_frames)

        if failed_count == 0:
            return {
                "job_id": job_id,
                "message": "No failed frames to retry"
            }

        # Reset failed frames back to pending
        frames_to_retry = job.failed_frames.copy()
        job.failed_frames = []

        self.logger.info(f"Retrying {failed_count} failed frames for job {job_id}")

        return {
            "job_id": job_id,
            "retried_frames": frames_to_retry,
            "retry_count": failed_count
        }

    def _list_jobs(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List render jobs, optionally filtered."""
        status_filter = params.get("status")
        shot_id = params.get("shot_id")

        jobs = []
        for job in self.render_jobs.values():
            if status_filter and job.status.value != status_filter:
                continue
            if shot_id and job.shot_id != shot_id:
                continue

            total_frames = len(job.frames)
            completed_frames = len(job.completed_frames)
            progress = (completed_frames / total_frames * 100) if total_frames > 0 else 0

            jobs.append({
                "job_id": job.id,
                "name": job.name,
                "shot_id": job.shot_id,
                "status": job.status.value,
                "priority": job.priority.value,
                "progress": round(progress, 2),
                "submitted_at": job.submitted_at.isoformat()
            })

        # Sort by priority (descending) then submission time
        jobs.sort(key=lambda x: (-x["priority"], x["submitted_at"]))

        return jobs

    def _get_farm_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get overall render farm status."""
        total_jobs = len(self.render_jobs)
        active_jobs = sum(1 for job in self.render_jobs.values()
                         if job.status == Status.IN_PROGRESS)
        pending_jobs = sum(1 for job in self.render_jobs.values()
                          if job.status == Status.PENDING)

        total_frames = sum(len(job.frames) for job in self.render_jobs.values())
        completed_frames = sum(len(job.completed_frames) for job in self.render_jobs.values())

        return {
            "farm_capacity": self.farm_capacity,
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "pending_jobs": pending_jobs,
            "total_frames": total_frames,
            "completed_frames": completed_frames,
            "utilization": round((active_jobs / self.farm_capacity * 100), 2) if self.farm_capacity > 0 else 0
        }

    def _monitor_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor a job and return progress updates."""
        job_id = params.get("job_id")

        if job_id not in self.render_jobs:
            raise ValueError(f"Render job not found: {job_id}")

        job = self.render_jobs[job_id]

        # In production, this would poll the actual render farm
        # For now, simulate progress
        if job.status == Status.PENDING:
            job.status = Status.IN_PROGRESS
            job.started_at = datetime.now()

        return self._get_job_status({"job_id": job_id})
