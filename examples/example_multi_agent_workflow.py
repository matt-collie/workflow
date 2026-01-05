"""
Example: Multi-Agent Coordination Workflow

This example demonstrates how multiple agents work together
in a complete VFX production workflow.
"""

from agents.asset import AssetAgent
from agents.shot import ShotAgent
from agents.render import RenderAgent
from agents.review import ReviewAgent
from agents.production import ProductionAgent


def main():
    """Run complete multi-agent workflow."""

    print("=== Multi-Agent VFX Pipeline Workflow ===\n")

    # Initialize all agents
    asset_agent = AssetAgent(config_path="config/agents.yaml")
    shot_agent = ShotAgent(config_path="config/agents.yaml")
    render_agent = RenderAgent(config_path="config/agents.yaml")
    review_agent = ReviewAgent(config_path="config/agents.yaml")
    production_agent = ProductionAgent(config_path="config/agents.yaml")

    print("✓ All agents initialized\n")

    # ========== ASSET CREATION PHASE ==========
    print("--- PHASE 1: Asset Creation ---\n")

    # Asset agent: Publish character
    print("1. Publishing hero character asset...")
    asset_result = asset_agent.execute_action(
        action="publish_asset",
        parameters={
            "name": "hero_main",
            "type": "character",
            "file_path": "/mnt/projects/work/assets/hero_main_v001.ma",
            "artist": "asset_artist",
            "department": "model"
        }
    )

    asset_id = asset_result.data['asset_id'] if asset_result.success else None
    print(f"   ✓ Asset published: {asset_id}\n")

    # ========== SHOT SETUP PHASE ==========
    print("--- PHASE 2: Shot Setup ---\n")

    # Shot agent: Create shot
    print("2. Creating shot with published assets...")
    shot_result = shot_agent.execute_action(
        action="create_shot",
        parameters={
            "sequence": "SQ020",
            "shot_number": "0030",
            "frame_start": 1001,
            "frame_end": 1120,
            "assets": [asset_id] if asset_id else []
        }
    )

    shot_id = shot_result.data['shot_id'] if shot_result.success else None
    print(f"   ✓ Shot created: {shot_id}")

    # Break down shot into tasks
    print("   Breaking down into department tasks...")
    shot_agent.execute_action(
        action="breakdown_shot",
        parameters={
            "shot_id": shot_id,
            "departments": ["layout", "animation", "lighting"]
        }
    )
    print("   ✓ Tasks created\n")

    # ========== PRODUCTION TRACKING ==========
    print("--- PHASE 3: Production Tracking ---\n")

    # Production agent: Track progress
    print("3. Tracking production progress...")
    progress_result = production_agent.execute_action(
        action="track_progress",
        parameters={
            "project_id": "project_alpha"
        }
    )

    if progress_result.success:
        progress = progress_result.data
        print(f"   Project Progress: {progress['completion_percentage']}%")
        print(f"   Completed Shots: {progress['completed_shots']}/{progress['total_shots']}")
        print(f"   On Schedule: {'Yes' if progress['on_schedule'] else 'No'}\n")

    # ========== RENDER SUBMISSION ==========
    print("--- PHASE 4: Render Submission ---\n")

    # Render agent: Submit lighting render
    print("4. Submitting lighting render...")
    render_result = render_agent.execute_action(
        action="submit_job",
        parameters={
            "shot_id": shot_id,
            "job_name": f"{shot_id}_lighting_beauty",
            "frames": list(range(1001, 1121)),
            "render_layer": "beauty",
            "output_path": f"/mnt/projects/render/{shot_id}/beauty",
            "priority": "HIGH",
            "submitted_by": "lighting_artist"
        }
    )

    job_id = render_result.data['job_id'] if render_result.success else None
    print(f"   ✓ Render job submitted: {job_id}")
    print(f"   Frames: {render_result.data['frame_count']}")
    print(f"   Priority: {render_result.data['priority']}\n")

    # Monitor render job
    print("5. Monitoring render progress...")
    monitor_result = render_agent.execute_action(
        action="monitor_job",
        parameters={
            "job_id": job_id
        }
    )

    if monitor_result.success:
        status = monitor_result.data
        print(f"   Status: {status['status']}")
        print(f"   Progress: {status['progress']}%\n")

    # ========== REVIEW SESSION ==========
    print("--- PHASE 5: Review & Approval ---\n")

    # Review agent: Create review session
    print("6. Creating review session...")
    review_result = review_agent.execute_action(
        action="create_review_session",
        parameters={
            "name": "Week 3 Dailies",
            "type": "internal",
            "shots": [shot_id],
            "reviewers": ["supervisor", "director", "lead_artist"],
            "scheduled_at": "2026-01-06T09:30:00"
        }
    )

    review_id = review_result.data['review_id'] if review_result.success else None
    print(f"   ✓ Review session created: {review_id}\n")

    # Add feedback
    print("7. Adding review feedback...")
    review_agent.execute_action(
        action="add_feedback",
        parameters={
            "review_id": review_id,
            "shot_id": shot_id,
            "reviewer": "supervisor",
            "comment": "Character performance looks great, slight adjustment needed on lighting",
            "frame_number": 1050,
            "severity": "minor"
        }
    )
    print("   ✓ Feedback added\n")

    # ========== PRODUCTION REPORT ==========
    print("--- PHASE 6: Production Reporting ---\n")

    # Production agent: Generate report
    print("8. Generating production report...")
    report_result = production_agent.execute_action(
        action="generate_report",
        parameters={
            "project_id": "project_alpha",
            "report_type": "weekly",
            "start_date": "2026-01-01",
            "end_date": "2026-01-05"
        }
    )

    if report_result.success:
        report = report_result.data
        print(f"   Report Type: {report['report_type']}")
        print(f"   Shots Completed: {report['summary']['shots_completed']}")
        print(f"   Assets Published: {report['summary']['assets_published']}")
        print(f"   Reviews Held: {report['summary']['reviews_held']}")
        print(f"   Render Hours: {report['summary']['render_hours']}\n")

    # Get farm status
    print("9. Checking render farm status...")
    farm_result = render_agent.execute_action(
        action="get_farm_status",
        parameters={}
    )

    if farm_result.success:
        farm = farm_result.data
        print(f"   Farm Capacity: {farm['farm_capacity']}")
        print(f"   Active Jobs: {farm['active_jobs']}")
        print(f"   Utilization: {farm['utilization']}%\n")

    # ========== WORKFLOW SUMMARY ==========
    print("--- Workflow Summary ---\n")
    print(f"✓ Asset Published: {asset_id}")
    print(f"✓ Shot Created: {shot_id}")
    print(f"✓ Render Job Submitted: {job_id}")
    print(f"✓ Review Session Scheduled: {review_id}")
    print(f"✓ Production Report Generated")

    print("\n=== Multi-Agent Workflow Complete ===")


if __name__ == "__main__":
    main()
