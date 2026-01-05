"""
Base data models for VFX pipeline agents.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any


class Status(Enum):
    """Common status values across pipeline."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    REVIEW = "review"
    APPROVED = "approved"
    FINAL = "final"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Priority levels for tasks and renders."""
    LOW = 1
    MEDIUM = 50
    HIGH = 75
    CRITICAL = 100


@dataclass
class Task:
    """Represents a production task."""
    id: str
    name: str
    department: str
    assignee: Optional[str] = None
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Asset:
    """Represents a VFX asset."""
    id: str
    name: str
    type: str  # character, prop, environment, etc.
    version: int
    status: Status
    artist: str
    department: str
    file_path: str
    thumbnail_path: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None


@dataclass
class Shot:
    """Represents a production shot."""
    id: str
    sequence: str
    number: str
    name: str
    status: Status
    frame_range: tuple[int, int]
    tasks: List[Task] = field(default_factory=list)
    assets: List[str] = field(default_factory=list)  # Asset IDs
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class RenderJob:
    """Represents a render job."""
    id: str
    shot_id: str
    name: str
    status: Status
    priority: Priority
    frames: List[int]
    completed_frames: List[int] = field(default_factory=list)
    failed_frames: List[int] = field(default_factory=list)
    render_layer: str = ""
    output_path: str = ""
    submitted_by: str = ""
    submitted_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Review:
    """Represents a review session."""
    id: str
    name: str
    type: str  # internal, client, director
    shots: List[str]  # Shot IDs
    reviewers: List[str]
    status: Status
    feedback: List[Dict[str, Any]] = field(default_factory=list)
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRequest:
    """Represents a request to an agent."""
    id: str
    agent_type: str
    action: str
    parameters: Dict[str, Any]
    requester: str
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentResponse:
    """Represents an agent's response."""
    request_id: str
    success: bool
    data: Any
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
