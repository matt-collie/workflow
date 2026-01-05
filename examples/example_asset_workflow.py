"""
Example: Asset Publishing Workflow

This example demonstrates how to use the AssetAgent to publish
and manage assets in a VFX pipeline.
"""

from agents.asset import AssetAgent


def main():
    """Run asset publishing workflow."""

    # Initialize the asset agent
    agent = AssetAgent(config_path="config/agents.yaml")

    print("=== Asset Publishing Workflow ===\n")

    # 1. Publish a new character asset
    print("1. Publishing new character asset...")
    publish_result = agent.execute_action(
        action="publish_asset",
        parameters={
            "name": "hero_character",
            "type": "character",
            "file_path": "/mnt/projects/work/assets/characters/hero_character_v001.ma",
            "artist": "john_doe",
            "department": "model"
        }
    )

    if publish_result.success:
        print(f"   ✓ Asset published: {publish_result.data['asset_id']}")
        asset_id = publish_result.data['asset_id']
    else:
        print(f"   ✗ Failed: {publish_result.message}")
        return

    # 2. Validate the asset
    print("\n2. Validating asset...")
    validation_result = agent.execute_action(
        action="validate_asset",
        parameters={
            "file_path": "/mnt/projects/work/assets/characters/hero_character_v001.ma",
            "type": "character"
        }
    )

    if validation_result.success:
        data = validation_result.data
        if data['is_valid']:
            print("   ✓ Asset validation passed")
            if data['warnings']:
                print(f"   ⚠ Warnings: {', '.join(data['warnings'])}")
        else:
            print(f"   ✗ Validation errors: {', '.join(data['errors'])}")

    # 3. Search for character assets
    print("\n3. Searching for character assets...")
    search_result = agent.execute_action(
        action="search_assets",
        parameters={
            "type": "character"
        }
    )

    if search_result.success:
        assets = search_result.data
        print(f"   Found {len(assets)} character assets:")
        for asset in assets[:3]:  # Show first 3
            print(f"   - {asset['name']} (v{asset['version']}) - {asset['status']}")

    # 4. Create a new version
    print("\n4. Creating new version...")
    version_result = agent.execute_action(
        action="version_asset",
        parameters={
            "asset_id": asset_id,
            "file_path": "/mnt/projects/work/assets/characters/hero_character_v002.ma"
        }
    )

    if version_result.success:
        print(f"   ✓ New version created: v{version_result.data['version']}")

    # 5. Update asset status to approved
    print("\n5. Updating asset status to approved...")
    status_result = agent.execute_action(
        action="update_asset_status",
        parameters={
            "asset_id": asset_id,
            "status": "approved"
        }
    )

    if status_result.success:
        print(f"   ✓ Status updated: {status_result.data['old_status']} → {status_result.data['new_status']}")

    # 6. Get detailed asset info
    print("\n6. Getting asset information...")
    info_result = agent.execute_action(
        action="get_asset_info",
        parameters={
            "asset_id": asset_id
        }
    )

    if info_result.success:
        info = info_result.data
        print(f"   Asset: {info['name']}")
        print(f"   Type: {info['type']}")
        print(f"   Version: {info['version']}")
        print(f"   Status: {info['status']}")
        print(f"   Artist: {info['artist']}")
        print(f"   Path: {info['file_path']}")

    print("\n=== Workflow Complete ===")


if __name__ == "__main__":
    main()
