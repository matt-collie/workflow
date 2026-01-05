"""
Asset Agent - Manages asset creation, versioning, and publishing.
"""
from typing import List, Dict, Any
from pathlib import Path

from shared.base_agent import BaseAgent
from shared.models import AgentRequest, AgentResponse, Asset, Status


class AssetAgent(BaseAgent):
    """
    Agent responsible for asset management in the VFX pipeline.

    Capabilities:
    - Asset publishing and versioning
    - Asset library management
    - Dependency tracking
    - Asset validation
    - Asset search and retrieval
    """

    def __init__(self, config_path: str = None):
        super().__init__("asset", config_path)
        self.asset_library = {}  # In production, this would be a database

    def _define_capabilities(self) -> List[str]:
        """Define asset agent capabilities."""
        return [
            "publish_asset",
            "version_asset",
            "search_assets",
            "validate_asset",
            "get_asset_dependencies",
            "update_asset_status",
            "list_assets",
            "get_asset_info",
        ]

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process asset-related requests."""
        action = request.action
        params = request.parameters

        try:
            if action == "publish_asset":
                result = self._publish_asset(params)
            elif action == "version_asset":
                result = self._version_asset(params)
            elif action == "search_assets":
                result = self._search_assets(params)
            elif action == "validate_asset":
                result = self._validate_asset(params)
            elif action == "get_asset_dependencies":
                result = self._get_dependencies(params)
            elif action == "update_asset_status":
                result = self._update_status(params)
            elif action == "list_assets":
                result = self._list_assets(params)
            elif action == "get_asset_info":
                result = self._get_asset_info(params)
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

    def _publish_asset(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Publish an asset to the library."""
        asset_name = params.get("name")
        asset_type = params.get("type")
        file_path = params.get("file_path")
        artist = params.get("artist")
        department = params.get("department", "model")

        # Validate asset
        validation_result = self._validate_asset({
            "file_path": file_path,
            "type": asset_type
        })

        if not validation_result["is_valid"]:
            raise ValueError(f"Asset validation failed: {validation_result['errors']}")

        # Create asset entry
        asset_id = f"{asset_type}_{asset_name}_v001"
        asset = Asset(
            id=asset_id,
            name=asset_name,
            type=asset_type,
            version=1,
            status=Status.REVIEW,
            artist=artist,
            department=department,
            file_path=file_path
        )

        # Store in library
        self.asset_library[asset_id] = asset

        self.logger.info(f"Published asset: {asset_id}")

        return {
            "asset_id": asset_id,
            "version": 1,
            "status": asset.status.value,
            "path": file_path
        }

    def _version_asset(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new version of an existing asset."""
        asset_id = params.get("asset_id")
        new_file_path = params.get("file_path")

        if asset_id not in self.asset_library:
            raise ValueError(f"Asset not found: {asset_id}")

        current_asset = self.asset_library[asset_id]
        new_version = current_asset.version + 1

        # Create new asset entry
        new_asset_id = asset_id.rsplit('_v', 1)[0] + f"_v{new_version:03d}"

        new_asset = Asset(
            id=new_asset_id,
            name=current_asset.name,
            type=current_asset.type,
            version=new_version,
            status=Status.REVIEW,
            artist=current_asset.artist,
            department=current_asset.department,
            file_path=new_file_path,
            tags=current_asset.tags.copy()
        )

        self.asset_library[new_asset_id] = new_asset

        return {
            "asset_id": new_asset_id,
            "version": new_version,
            "previous_version": current_asset.version
        }

    def _search_assets(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for assets by criteria."""
        query = params.get("query", "")
        asset_type = params.get("type")
        department = params.get("department")

        results = []
        for asset in self.asset_library.values():
            if query and query.lower() not in asset.name.lower():
                continue
            if asset_type and asset.type != asset_type:
                continue
            if department and asset.department != department:
                continue

            results.append({
                "id": asset.id,
                "name": asset.name,
                "type": asset.type,
                "version": asset.version,
                "status": asset.status.value,
                "artist": asset.artist
            })

        return results

    def _validate_asset(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate asset structure and naming."""
        file_path = params.get("file_path")
        asset_type = params.get("type")

        errors = []
        warnings = []

        # Check file exists
        if file_path and not Path(file_path).exists():
            errors.append(f"File not found: {file_path}")

        # Check naming convention
        # In production, this would check studio naming standards

        # Check file format
        if file_path:
            ext = Path(file_path).suffix
            valid_extensions = {
                "character": [".ma", ".mb", ".fbx"],
                "prop": [".ma", ".mb", ".fbx"],
                "environment": [".ma", ".mb", ".usd"],
            }

            if asset_type in valid_extensions:
                if ext not in valid_extensions[asset_type]:
                    warnings.append(f"Unusual file format for {asset_type}: {ext}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    def _get_dependencies(self, params: Dict[str, Any]) -> List[str]:
        """Get asset dependencies."""
        asset_id = params.get("asset_id")

        if asset_id not in self.asset_library:
            raise ValueError(f"Asset not found: {asset_id}")

        asset = self.asset_library[asset_id]
        return asset.dependencies

    def _update_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update asset status."""
        asset_id = params.get("asset_id")
        new_status = params.get("status")

        if asset_id not in self.asset_library:
            raise ValueError(f"Asset not found: {asset_id}")

        asset = self.asset_library[asset_id]
        old_status = asset.status

        # Convert string to Status enum
        if isinstance(new_status, str):
            new_status = Status[new_status.upper()]

        asset.status = new_status

        return {
            "asset_id": asset_id,
            "old_status": old_status.value,
            "new_status": new_status.value
        }

    def _list_assets(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List all assets."""
        return [
            {
                "id": asset.id,
                "name": asset.name,
                "type": asset.type,
                "version": asset.version,
                "status": asset.status.value
            }
            for asset in self.asset_library.values()
        ]

    def _get_asset_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed asset information."""
        asset_id = params.get("asset_id")

        if asset_id not in self.asset_library:
            raise ValueError(f"Asset not found: {asset_id}")

        asset = self.asset_library[asset_id]

        return {
            "id": asset.id,
            "name": asset.name,
            "type": asset.type,
            "version": asset.version,
            "status": asset.status.value,
            "artist": asset.artist,
            "department": asset.department,
            "file_path": asset.file_path,
            "tags": asset.tags,
            "dependencies": asset.dependencies,
            "created_at": asset.created_at.isoformat(),
            "published_at": asset.published_at.isoformat() if asset.published_at else None
        }
