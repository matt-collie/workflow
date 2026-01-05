"""
Review Agent - Manages review sessions, feedback, and approvals.
"""
from typing import List, Dict, Any
from datetime import datetime

from shared.base_agent import BaseAgent
from shared.models import AgentRequest, AgentResponse, Review, Status


class ReviewAgent(BaseAgent):
    """
    Agent responsible for review and approval workflows.

    Capabilities:
    - Review session scheduling
    - Feedback collection and routing
    - Approval tracking
    - Dailies management
    - Client review coordination
    """

    def __init__(self, config_path: str = None):
        super().__init__("review", config_path)
        self.reviews = {}  # In production, this would interface with RV/Syncsketch

    def _define_capabilities(self) -> List[str]:
        """Define review agent capabilities."""
        return [
            "create_review_session",
            "add_feedback",
            "approve_shot",
            "schedule_dailies",
            "list_reviews",
            "get_review_feedback",
            "update_review_status",
        ]

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process review-related requests."""
        action = request.action
        params = request.parameters

        try:
            if action == "create_review_session":
                result = self._create_review_session(params)
            elif action == "add_feedback":
                result = self._add_feedback(params)
            elif action == "approve_shot":
                result = self._approve_shot(params)
            elif action == "schedule_dailies":
                result = self._schedule_dailies(params)
            elif action == "list_reviews":
                result = self._list_reviews(params)
            elif action == "get_review_feedback":
                result = self._get_review_feedback(params)
            elif action == "update_review_status":
                result = self._update_review_status(params)
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

    def _create_review_session(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new review session."""
        name = params.get("name")
        review_type = params.get("type", "internal")  # internal, client, director
        shots = params.get("shots", [])
        reviewers = params.get("reviewers", [])
        scheduled_at = params.get("scheduled_at")

        review_id = f"review_{review_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        review = Review(
            id=review_id,
            name=name,
            type=review_type,
            shots=shots,
            reviewers=reviewers,
            status=Status.PENDING,
            scheduled_at=datetime.fromisoformat(scheduled_at) if scheduled_at else None
        )

        self.reviews[review_id] = review

        self.logger.info(f"Created review session: {review_id} with {len(shots)} shots")

        return {
            "review_id": review_id,
            "name": name,
            "type": review_type,
            "shot_count": len(shots),
            "status": review.status.value
        }

    def _add_feedback(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add feedback to a review session."""
        review_id = params.get("review_id")
        shot_id = params.get("shot_id")
        reviewer = params.get("reviewer")
        comment = params.get("comment")
        frame_number = params.get("frame_number")
        severity = params.get("severity", "note")  # note, minor, major, critical

        if review_id not in self.reviews:
            raise ValueError(f"Review not found: {review_id}")

        review = self.reviews[review_id]

        feedback_item = {
            "shot_id": shot_id,
            "reviewer": reviewer,
            "comment": comment,
            "frame_number": frame_number,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "status": "open"
        }

        review.feedback.append(feedback_item)

        self.logger.info(f"Added feedback to review {review_id} for shot {shot_id}")

        return {
            "review_id": review_id,
            "shot_id": shot_id,
            "feedback_count": len(review.feedback)
        }

    def _approve_shot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Approve a shot in a review session."""
        review_id = params.get("review_id")
        shot_id = params.get("shot_id")
        approver = params.get("approver")

        if review_id not in self.reviews:
            raise ValueError(f"Review not found: {review_id}")

        review = self.reviews[review_id]

        approval_item = {
            "shot_id": shot_id,
            "approver": approver,
            "approved_at": datetime.now().isoformat(),
            "status": "approved"
        }

        review.feedback.append(approval_item)

        self.logger.info(f"Shot {shot_id} approved in review {review_id} by {approver}")

        return {
            "review_id": review_id,
            "shot_id": shot_id,
            "approver": approver,
            "status": "approved"
        }

    def _schedule_dailies(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a dailies session."""
        date = params.get("date")
        shots = params.get("shots", [])
        attendees = params.get("attendees", [])

        dailies_name = f"Dailies {date}"

        return self._create_review_session({
            "name": dailies_name,
            "type": "internal",
            "shots": shots,
            "reviewers": attendees,
            "scheduled_at": date
        })

    def _list_reviews(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List review sessions."""
        review_type = params.get("type")
        status_filter = params.get("status")

        reviews = []
        for review in self.reviews.values():
            if review_type and review.type != review_type:
                continue
            if status_filter and review.status.value != status_filter:
                continue

            reviews.append({
                "review_id": review.id,
                "name": review.name,
                "type": review.type,
                "status": review.status.value,
                "shot_count": len(review.shots),
                "feedback_count": len(review.feedback),
                "scheduled_at": review.scheduled_at.isoformat() if review.scheduled_at else None
            })

        return reviews

    def _get_review_feedback(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all feedback for a review session."""
        review_id = params.get("review_id")
        shot_id = params.get("shot_id")

        if review_id not in self.reviews:
            raise ValueError(f"Review not found: {review_id}")

        review = self.reviews[review_id]

        feedback = review.feedback
        if shot_id:
            feedback = [f for f in feedback if f.get("shot_id") == shot_id]

        return feedback

    def _update_review_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update review session status."""
        review_id = params.get("review_id")
        new_status = params.get("status")

        if review_id not in self.reviews:
            raise ValueError(f"Review not found: {review_id}")

        review = self.reviews[review_id]
        old_status = review.status

        if isinstance(new_status, str):
            new_status = Status[new_status.upper()]

        review.status = new_status

        if new_status in [Status.APPROVED, Status.FINAL]:
            review.completed_at = datetime.now()

        return {
            "review_id": review_id,
            "old_status": old_status.value,
            "new_status": new_status.value
        }
