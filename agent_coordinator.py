"""
Agent Coordinator - Central coordination for multi-agent workflows.

This module provides a central coordinator that manages communication
and orchestration between different agents in the VFX pipeline.
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from agents import (
    AssetAgent,
    ShotAgent,
    RenderAgent,
    ReviewAgent,
    PipelineAgent,
    ProductionAgent
)
from shared.models import AgentRequest, AgentResponse


class AgentCoordinator:
    """
    Coordinates operations between multiple agents.

    The coordinator acts as a central hub for multi-agent workflows,
    routing requests to appropriate agents and managing inter-agent
    communication.
    """

    def __init__(self, config_path: str = "config/agents.yaml"):
        """
        Initialize the agent coordinator.

        Args:
            config_path: Path to agent configuration file
        """
        self.config_path = config_path
        self.logger = self._setup_logging()

        # Initialize all agents
        self.agents: Dict[str, Any] = {}
        self._initialize_agents()

        self.logger.info("Agent Coordinator initialized with all agents")

    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the coordinator."""
        logger = logging.getLogger("coordinator")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - COORDINATOR - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_agents(self):
        """Initialize all available agents."""
        agent_classes = {
            "asset": AssetAgent,
            "shot": ShotAgent,
            "render": RenderAgent,
            "review": ReviewAgent,
            "pipeline": PipelineAgent,
            "production": ProductionAgent
        }

        for agent_type, agent_class in agent_classes.items():
            try:
                self.agents[agent_type] = agent_class(config_path=self.config_path)
                self.logger.info(f"Initialized {agent_type} agent")
            except Exception as e:
                self.logger.error(f"Failed to initialize {agent_type} agent: {e}")

    def route_request(
        self,
        agent_type: str,
        action: str,
        parameters: Dict[str, Any]
    ) -> AgentResponse:
        """
        Route a request to the appropriate agent.

        Args:
            agent_type: Type of agent to route to
            action: Action to perform
            parameters: Action parameters

        Returns:
            AgentResponse from the agent
        """
        if agent_type not in self.agents:
            self.logger.error(f"Unknown agent type: {agent_type}")
            return AgentResponse(
                request_id="",
                success=False,
                data=None,
                message=f"Unknown agent type: {agent_type}"
            )

        agent = self.agents[agent_type]
        self.logger.info(f"Routing {action} to {agent_type} agent")

        return agent.execute_action(action, parameters)

    def execute_workflow(
        self,
        workflow_name: str,
        workflow_steps: List[Dict[str, Any]]
    ) -> List[AgentResponse]:
        """
        Execute a multi-step workflow across multiple agents.

        Args:
            workflow_name: Name of the workflow
            workflow_steps: List of workflow steps, each containing:
                - agent: Agent type
                - action: Action to perform
                - parameters: Action parameters

        Returns:
            List of AgentResponse objects, one per step
        """
        self.logger.info(f"Executing workflow: {workflow_name}")
        results = []

        for idx, step in enumerate(workflow_steps, 1):
            self.logger.info(f"Step {idx}/{len(workflow_steps)}: {step['action']}")

            response = self.route_request(
                agent_type=step['agent'],
                action=step['action'],
                parameters=step.get('parameters', {})
            )

            results.append(response)

            if not response.success:
                self.logger.error(
                    f"Workflow step {idx} failed: {response.message}"
                )
                # Optionally stop workflow on failure
                # break

        self.logger.info(f"Workflow {workflow_name} completed")
        return results

    def get_agent_status(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get status of one or all agents.

        Args:
            agent_type: Specific agent to check, or None for all

        Returns:
            Status dictionary
        """
        if agent_type:
            if agent_type in self.agents:
                return self.agents[agent_type].get_status()
            return {"error": f"Unknown agent type: {agent_type}"}

        # Get status of all agents
        return {
            agent_type: agent.get_status()
            for agent_type, agent in self.agents.items()
        }

    def execute_asset_to_render_workflow(
        self,
        asset_name: str,
        shot_id: str,
        render_layer: str = "beauty"
    ) -> Dict[str, Any]:
        """
        Example coordinated workflow: Asset publishing through render submission.

        Args:
            asset_name: Name of asset to publish
            shot_id: Shot to render
            render_layer: Render layer name

        Returns:
            Workflow results
        """
        workflow_steps = [
            {
                "agent": "asset",
                "action": "publish_asset",
                "parameters": {
                    "name": asset_name,
                    "type": "character",
                    "file_path": f"/mnt/work/{asset_name}.ma",
                    "artist": "system",
                    "department": "model"
                }
            },
            {
                "agent": "shot",
                "action": "update_shot_status",
                "parameters": {
                    "shot_id": shot_id,
                    "status": "ready_to_render"
                }
            },
            {
                "agent": "render",
                "action": "submit_job",
                "parameters": {
                    "shot_id": shot_id,
                    "job_name": f"{shot_id}_{render_layer}",
                    "frames": list(range(1001, 1101)),
                    "render_layer": render_layer,
                    "output_path": f"/mnt/render/{shot_id}",
                    "priority": "MEDIUM",
                    "submitted_by": "coordinator"
                }
            },
            {
                "agent": "production",
                "action": "track_progress",
                "parameters": {
                    "project_id": "default_project"
                }
            }
        ]

        results = self.execute_workflow(
            "asset_to_render",
            workflow_steps
        )

        return {
            "workflow": "asset_to_render",
            "steps_completed": len([r for r in results if r.success]),
            "total_steps": len(results),
            "results": [
                {
                    "success": r.success,
                    "message": r.message,
                    "data": r.data
                }
                for r in results
            ]
        }


def main():
    """Example usage of the Agent Coordinator."""
    coordinator = AgentCoordinator()

    print("\n=== Agent Coordinator Example ===\n")

    # Get status of all agents
    print("1. Checking agent status...")
    status = coordinator.get_agent_status()
    for agent_type, agent_status in status.items():
        print(f"   {agent_type}: {agent_status['status']}")

    # Execute a single action
    print("\n2. Creating a shot via coordinator...")
    response = coordinator.route_request(
        agent_type="shot",
        action="create_shot",
        parameters={
            "sequence": "SQ100",
            "shot_number": "0010",
            "frame_start": 1001,
            "frame_end": 1150
        }
    )
    print(f"   Success: {response.success}")
    if response.success:
        print(f"   Shot ID: {response.data['shot_id']}")

    # Execute a coordinated workflow
    print("\n3. Executing coordinated workflow...")
    workflow_result = coordinator.execute_asset_to_render_workflow(
        asset_name="hero_character",
        shot_id="SQ100_0010",
        render_layer="beauty"
    )
    print(f"   Completed: {workflow_result['steps_completed']}/{workflow_result['total_steps']} steps")

    print("\n=== Coordinator Example Complete ===\n")


if __name__ == "__main__":
    main()
