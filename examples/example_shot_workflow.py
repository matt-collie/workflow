"""
Example: Shot Production Workflow

This example demonstrates how to use the ShotAgent to manage
shot production and task assignment.
"""

from agents.shot import ShotAgent


def main():
    """Run shot production workflow."""

    # Initialize the shot agent
    agent = ShotAgent(config_path="config/agents.yaml")

    print("=== Shot Production Workflow ===\n")

    # 1. Create a new shot
    print("1. Creating new shot...")
    create_result = agent.execute_action(
        action="create_shot",
        parameters={
            "sequence": "SQ010",
            "shot_number": "0010",
            "frame_start": 1001,
            "frame_end": 1150,
            "assets": ["character_hero_v003", "prop_sword_v001"]
        }
    )

    if create_result.success:
        print(f"   ✓ Shot created: {create_result.data['shot_id']}")
        shot_id = create_result.data['shot_id']
    else:
        print(f"   ✗ Failed: {create_result.message}")
        return

    # 2. Break down the shot into department tasks
    print("\n2. Breaking down shot into tasks...")
    breakdown_result = agent.execute_action(
        action="breakdown_shot",
        parameters={
            "shot_id": shot_id,
            "departments": ["layout", "animation", "fx", "lighting", "comp"]
        }
    )

    if breakdown_result.success:
        tasks = breakdown_result.data
        print(f"   ✓ Created {len(tasks)} tasks:")
        for task in tasks:
            print(f"   - {task['department']}: {task['task_id']}")

    # 3. Assign tasks to artists
    print("\n3. Assigning tasks to artists...")

    assignments = [
        ("layout", "jane_smith"),
        ("animation", "mike_jones"),
        ("fx", "sarah_lee"),
        ("lighting", "tom_brown"),
        ("comp", "lisa_chen")
    ]

    for dept, artist in assignments:
        assign_result = agent.execute_action(
            action="assign_task",
            parameters={
                "shot_id": shot_id,
                "task_name": f"{dept}_task",
                "department": dept,
                "assignee": artist,
                "priority": "HIGH" if dept in ["lighting", "comp"] else "MEDIUM"
            }
        )

        if assign_result.success:
            print(f"   ✓ Assigned {dept} to {artist}")

    # 4. Get all tasks for the shot
    print("\n4. Retrieving shot tasks...")
    tasks_result = agent.execute_action(
        action="get_shot_tasks",
        parameters={
            "shot_id": shot_id
        }
    )

    if tasks_result.success:
        tasks = tasks_result.data
        print(f"   Found {len(tasks)} tasks:")
        for task in tasks[:5]:  # Show first 5
            print(f"   - {task['department']}: {task['assignee']} (Priority: {task['priority']})")

    # 5. Update shot status
    print("\n5. Updating shot status to in_progress...")
    status_result = agent.execute_action(
        action="update_shot_status",
        parameters={
            "shot_id": shot_id,
            "status": "in_progress"
        }
    )

    if status_result.success:
        print(f"   ✓ Status updated: {status_result.data['new_status']}")

    # 6. Get detailed shot information
    print("\n6. Getting shot information...")
    info_result = agent.execute_action(
        action="get_shot_info",
        parameters={
            "shot_id": shot_id
        }
    )

    if info_result.success:
        info = info_result.data
        print(f"   Shot: {info['name']}")
        print(f"   Sequence: {info['sequence']}")
        print(f"   Status: {info['status']}")
        print(f"   Frame Range: {info['frame_range'][0]}-{info['frame_range'][1]}")
        print(f"   Assets: {', '.join(info['assets'])}")
        print(f"   Tasks: {len(info['tasks'])}")

    # 7. List all shots in sequence
    print("\n7. Listing all shots in sequence...")
    list_result = agent.execute_action(
        action="get_sequence_shots",
        parameters={
            "sequence": "SQ010"
        }
    )

    if list_result.success:
        shots = list_result.data
        print(f"   Found {len(shots)} shots in SQ010:")
        for shot in shots:
            print(f"   - {shot['id']}: {shot['status']}")

    print("\n=== Workflow Complete ===")


if __name__ == "__main__":
    main()
