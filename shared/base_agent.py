"""
Base agent class for VFX pipeline agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import yaml
from pathlib import Path

from shared.models import AgentRequest, AgentResponse, Priority


class BaseAgent(ABC):
    """
    Abstract base class for all VFX pipeline agents.

    All specialized agents (Asset, Shot, Render, etc.) inherit from this class
    and implement their specific capabilities.
    """

    def __init__(
        self,
        agent_name: str,
        config_path: Optional[str] = None,
        log_level: str = "INFO"
    ):
        """
        Initialize the base agent.

        Args:
            agent_name: Name of the agent (e.g., "asset", "render")
            config_path: Path to configuration file
            log_level: Logging level
        """
        self.agent_name = agent_name
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging(log_level)
        self.capabilities = self._define_capabilities()

        self.logger.info(f"{self.agent_name} agent initialized")

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load agent configuration from YAML file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get(self.agent_name, {})
        return {}

    def _setup_logging(self, log_level: str) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(f"agent.{self.agent_name}")
        logger.setLevel(getattr(logging, log_level.upper()))

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.agent_name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @abstractmethod
    def _define_capabilities(self) -> List[str]:
        """
        Define the capabilities of this agent.

        Returns:
            List of capability names
        """
        pass

    @abstractmethod
    def process_request(self, request: AgentRequest) -> AgentResponse:
        """
        Process an incoming request.

        Args:
            request: The agent request to process

        Returns:
            AgentResponse with results
        """
        pass

    def can_handle(self, action: str) -> bool:
        """
        Check if this agent can handle a specific action.

        Args:
            action: The action to check

        Returns:
            True if agent can handle this action
        """
        return action in self.capabilities

    def validate_request(self, request: AgentRequest) -> tuple[bool, Optional[str]]:
        """
        Validate an incoming request.

        Args:
            request: The request to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.can_handle(request.action):
            return False, f"Agent {self.agent_name} cannot handle action: {request.action}"

        return True, None

    def execute_action(
        self,
        action: str,
        parameters: Dict[str, Any]
    ) -> AgentResponse:
        """
        Execute a specific action with parameters.

        Args:
            action: Action to execute
            parameters: Action parameters

        Returns:
            AgentResponse with results
        """
        self.logger.info(f"Executing action: {action}")

        # Create request object
        request = AgentRequest(
            id=self._generate_request_id(),
            agent_type=self.agent_name,
            action=action,
            parameters=parameters,
            requester="system"
        )

        # Validate and process
        is_valid, error = self.validate_request(request)
        if not is_valid:
            return AgentResponse(
                request_id=request.id,
                success=False,
                data=None,
                message=error
            )

        return self.process_request(request)

    def _generate_request_id(self) -> str:
        """Generate a unique request ID."""
        import uuid
        return f"{self.agent_name}_{uuid.uuid4().hex[:8]}"

    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the agent.

        Returns:
            Status dictionary
        """
        return {
            "agent_name": self.agent_name,
            "capabilities": self.capabilities,
            "status": "running"
        }
