"""Asset management operations.

Provides CRUD operations for assets that extend the official SDK's
retrieve and update capabilities.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class AssetsExt:
    """Extensions for Asset operations.

    The official SDK provides basic asset retrieval and updates, but is missing:
    - Listing assets with filtering
    - Creating new assets
    - Deleting assets
    - Cross-folder asset operations

    This extension fills those gaps using the OData endpoints.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_assets(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List all assets in a folder with optional filtering.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "Name eq 'MyAsset'")
            top: Maximum number of results to return
            skip: Number of results to skip (for pagination)

        Returns:
            List of asset dictionaries with Name, ValueType, Value, etc.

        Raises:
            Exception: If API request fails

        Example:
            >>> assets = AssetsExt(sdk)
            >>> all_assets = assets.list_assets(folder_key="5ebb73c3-...")
            >>> for asset in all_assets:
            ...     print(f"{asset['Name']}: {asset['ValueType']}")
            >>>
            >>> # Filter for credential assets only
            >>> creds = assets.list_assets(
            ...     folder_key="5ebb73c3-...",
            ...     filter_query="ValueType eq 'Credential'"
            ... )
        """
        params = {}
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/Assets",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def create_asset(
        self,
        name: str,
        value_type: str,
        value: Any,
        folder_key: Optional[str] = None,
        description: Optional[str] = None,
        can_be_deleted: bool = True
    ) -> Dict[str, Any]:
        """Create a new asset.

        Args:
            name: Asset name (must be unique in folder)
            value_type: Asset type - "Text", "Bool", "Integer", "Credential", "WindowsCredential", "KeyValueList", "DBConnectionString"
            value: Asset value (format depends on value_type)
            folder_key: Folder GUID (optional - uses current folder if not specified)
            description: Asset description (optional)
            can_be_deleted: Whether asset can be deleted (default: True)

        Returns:
            Created asset dictionary

        Raises:
            Exception: If API request fails or asset already exists

        Example:
            >>> assets = AssetsExt(sdk)
            >>> # Create text asset
            >>> text_asset = assets.create_asset(
            ...     name="APIEndpoint",
            ...     value_type="Text",
            ...     value="https://api.example.com",
            ...     folder_key="5ebb73c3-...",
            ...     description="Production API endpoint"
            ... )
            >>>
            >>> # Create credential asset
            >>> cred_asset = assets.create_asset(
            ...     name="DatabaseCreds",
            ...     value_type="Credential",
            ...     value={"Username": "admin", "Password": "secret"},
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "Name": name,
            "ValueType": value_type,
            "Value": value,
            "CanBeDeleted": can_be_deleted
        }

        if description:
            payload["Description"] = description

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/odata/Assets",
            json=payload,
            headers=headers
        )

        return response.json()

    def delete_asset(self, asset_key: str, folder_key: Optional[str] = None) -> None:
        """Delete an asset by key.

        Args:
            asset_key: Asset GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails or asset not found

        Example:
            >>> assets = AssetsExt(sdk)
            >>> assets.delete_asset(
            ...     asset_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "DELETE",
            f"/odata/Assets({asset_key})",
            headers=headers
        )

    def get_asset_by_name(
        self,
        name: str,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get asset by name.

        Args:
            name: Asset name
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Asset dictionary or None if not found

        Example:
            >>> assets = AssetsExt(sdk)
            >>> asset = assets.get_asset_by_name(
            ...     name="MyAsset",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if asset:
            ...     print(f"Found: {asset['ValueType']}")
        """
        assets = self.list_assets(
            folder_key=folder_key,
            filter_query=f"Name eq '{name}'"
        )

        return assets[0] if assets else None

    def get_assets_across_folders(
        self,
        asset_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get assets across all accessible folders.

        Args:
            asset_name: Optional asset name filter

        Returns:
            List of asset dictionaries with folder information

        Raises:
            Exception: If API request fails

        Example:
            >>> assets = AssetsExt(sdk)
            >>> # Find all instances of an asset across folders
            >>> instances = assets.get_assets_across_folders(
            ...     asset_name="DatabaseCreds"
            ... )
            >>> for asset in instances:
            ...     print(f"{asset['FolderPath']}: {asset['Name']}")
        """
        params = {}
        if asset_name:
            params["assetName"] = asset_name

        response = self.sdk.api_client.request(
            "GET",
            "/odata/Assets/UiPath.Server.Configuration.OData.GetAssetsAcrossFolders",
            params=params
        )

        return response.json().get("value", [])

    def share_asset_to_folders(
        self,
        asset_key: str,
        folder_ids: List[int],
        source_folder_key: Optional[str] = None
    ) -> None:
        """Share an asset to multiple folders.

        Args:
            asset_key: Asset GUID key
            folder_ids: List of numeric folder IDs to share to
            source_folder_key: Source folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails

        Example:
            >>> assets = AssetsExt(sdk)
            >>> assets.share_asset_to_folders(
            ...     asset_key="a1b2c3d4-...",
            ...     folder_ids=[5083200, 5083201],
            ...     source_folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "assetId": asset_key,
            "folderIds": folder_ids
        }

        headers = {}
        if source_folder_key:
            headers["x-uipath-folderkey"] = source_folder_key

        self.sdk.api_client.request(
            "POST",
            "/odata/Assets/UiPath.Server.Configuration.OData.ShareToFolders",
            json=payload,
            headers=headers
        )

    def get_folders_for_asset(
        self,
        asset_key: str,
        source_folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all folders an asset is shared to.

        Args:
            asset_key: Asset GUID key
            source_folder_key: Source folder GUID (optional - uses current folder if not specified)

        Returns:
            List of folder dictionaries

        Raises:
            Exception: If API request fails

        Example:
            >>> assets = AssetsExt(sdk)
            >>> folders = assets.get_folders_for_asset(
            ...     asset_key="a1b2c3d4-...",
            ...     source_folder_key="5ebb73c3-..."
            ... )
            >>> for folder in folders:
            ...     print(f"Shared to: {folder['DisplayName']}")
        """
        params = {"assetId": asset_key}

        headers = {}
        if source_folder_key:
            headers["x-uipath-folderkey"] = source_folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/Assets/UiPath.Server.Configuration.OData.GetFoldersForAsset",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])
