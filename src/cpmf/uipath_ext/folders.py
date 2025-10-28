"""Folder management and navigation operations.

Provides CRUD operations for folders that extend the basic
folder utilities (FolderUtils) with full management capabilities.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath

from .folder_utils import FolderUtils


class FolderManagementExt:
    """Extensions for Folder management operations.

    Builds on FolderUtils to add:
    - Creating and deleting folders
    - Updating folder metadata
    - Folder hierarchy navigation
    - Permission and role management
    - Cross-folder operations

    For basic ID/Key conversion, use FolderUtils directly.
    For full CRUD and management, use this class.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk
        self.folder_utils = FolderUtils(sdk)

    def create_folder(
        self,
        display_name: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        provision_type: str = "Manual"
    ) -> Dict[str, Any]:
        """Create a new folder.

        Args:
            display_name: Folder display name
            description: Folder description (optional)
            parent_id: Parent folder ID for subfolder (optional - creates top-level if not specified)
            provision_type: Provisioning type - "Manual" or "Automatic" (default: "Manual")

        Returns:
            Created folder dictionary with Id, Key, DisplayName, etc.

        Raises:
            Exception: If API request fails

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> new_folder = folders.create_folder(
            ...     display_name="Production",
            ...     description="Production environment folder"
            ... )
            >>> print(f"Created folder: {new_folder['Key']}")
            >>>
            >>> # Create subfolder
            >>> subfolder = folders.create_folder(
            ...     display_name="US-Region",
            ...     description="US regional folder",
            ...     parent_id=new_folder['Id']
            ... )
        """
        payload = {
            "DisplayName": display_name,
            "ProvisionType": provision_type
        }

        if description:
            payload["Description"] = description
        if parent_id:
            payload["ParentId"] = parent_id

        response = self.sdk.api_client.request(
            "POST",
            "/odata/Folders",
            json=payload
        )

        # Clear cache since folder list changed
        self.folder_utils.clear_cache()

        return response.json()

    def delete_folder(
        self,
        folder_key: str
    ) -> None:
        """Delete a folder by key.

        Args:
            folder_key: Folder GUID key

        Raises:
            Exception: If API request fails or folder not found

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> folders.delete_folder(folder_key="a1b2c3d4-...")
        """
        response = self.sdk.api_client.request(
            "DELETE",
            f"/api/Folders/DeleteByKey",
            params={"key": folder_key}
        )

        # Clear cache since folder list changed
        self.folder_utils.clear_cache()

    def update_folder(
        self,
        folder_key: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """Update folder name and/or description.

        Args:
            folder_key: Folder GUID key
            display_name: New display name (optional)
            description: New description (optional)

        Raises:
            Exception: If API request fails or folder not found

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> folders.update_folder(
            ...     folder_key="5ebb73c3-...",
            ...     display_name="Production (US)",
            ...     description="Updated description"
            ... )
        """
        payload = {"Key": folder_key}

        if display_name is not None:
            payload["DisplayName"] = display_name
        if description is not None:
            payload["Description"] = description

        self.sdk.api_client.request(
            "PATCH",
            "/api/Folders/PatchNameDescription",
            json=payload
        )

        # Clear cache since folder metadata changed
        self.folder_utils.clear_cache()

    def get_folder_hierarchy(
        self,
        root_folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get folder hierarchy tree structure.

        Args:
            root_folder_key: Root folder GUID (optional - gets all folders if not specified)

        Returns:
            Dictionary representing folder tree with nested children

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> tree = folders.get_folder_hierarchy()
            >>> def print_tree(folder, indent=0):
            ...     print("  " * indent + folder['DisplayName'])
            ...     for child in folder.get('Children', []):
            ...         print_tree(child, indent + 1)
            >>> print_tree(tree)
        """
        all_folders = self.folder_utils.list_all_folders(use_cache=True)

        # Build parent-child relationships
        folders_by_id = {f['Id']: {**f, 'Children': []} for f in all_folders}

        # Find root folders
        root_folders = []
        for folder in all_folders:
            parent_id = folder.get('ParentId')
            if parent_id and parent_id in folders_by_id:
                folders_by_id[parent_id]['Children'].append(folders_by_id[folder['Id']])
            else:
                root_folders.append(folders_by_id[folder['Id']])

        # If specific root requested, find it
        if root_folder_key:
            for folder in all_folders:
                if folder['Key'] == root_folder_key:
                    return folders_by_id[folder['Id']]
            return {}

        # Return all root folders
        return {
            'Folders': root_folders,
            'TotalCount': len(all_folders)
        }

    def get_user_folder_roles(
        self
    ) -> List[Dict[str, Any]]:
        """Get all folders for current user with their roles.

        Returns:
            List of folder dictionaries with role information

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> user_folders = folders.get_user_folder_roles()
            >>> for folder in user_folders:
            ...     print(f"{folder['FolderPath']}: {folder['UserRole']}")
        """
        response = self.sdk.api_client.request(
            "GET",
            "/api/FoldersNavigation/GetFoldersForCurrentUser"
        )

        return response.json()

    def get_all_folders_for_user(
        self
    ) -> List[Dict[str, Any]]:
        """Get all accessible folders for current user (simplified).

        Returns:
            List of folder dictionaries

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> accessible = folders.get_all_folders_for_user()
            >>> print(f"User has access to {len(accessible)} folders")
        """
        response = self.sdk.api_client.request(
            "GET",
            "/api/Folders/GetAllForCurrentUser"
        )

        return response.json()

    def get_folder_navigation_context(
        self
    ) -> Dict[str, Any]:
        """Get folder navigation context for current user.

        Returns complete navigation context including breadcrumbs and permissions.

        Returns:
            Dictionary with navigation context

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> context = folders.get_folder_navigation_context()
            >>> print(f"Current folder: {context.get('CurrentFolder')}")
        """
        response = self.sdk.api_client.request(
            "GET",
            "/api/FoldersNavigation/GetFolderNavigationContextForCurrentUser"
        )

        return response.json()

    def get_all_roles_for_user(
        self
    ) -> List[Dict[str, Any]]:
        """Get all roles assigned to current user across folders.

        Returns:
            List of role dictionaries

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> roles = folders.get_all_roles_for_user()
            >>> for role in roles:
            ...     print(f"Folder: {role.get('FolderName')}, Role: {role.get('RoleName')}")
        """
        response = self.sdk.api_client.request(
            "GET",
            "/api/FoldersNavigation/GetAllRolesForUser"
        )

        return response.json()

    def move_folder(
        self,
        folder_id: int,
        new_parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Move folder to a new parent (or to root level).

        Args:
            folder_id: Folder ID to move
            new_parent_id: New parent folder ID (None for root level)

        Returns:
            Updated folder dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> # Move to root level
            >>> folders.move_folder(folder_id=12345, new_parent_id=None)
            >>>
            >>> # Move to different parent
            >>> folders.move_folder(folder_id=12345, new_parent_id=67890)
        """
        payload = {"ParentId": new_parent_id}

        response = self.sdk.api_client.request(
            "PATCH",
            f"/odata/Folders({folder_id})",
            json=payload
        )

        # Clear cache since hierarchy changed
        self.folder_utils.clear_cache()

        return response.json()

    def search_folders(
        self,
        search_term: str
    ) -> List[Dict[str, Any]]:
        """Search folders by name or description.

        Args:
            search_term: Search term to match against DisplayName or Description

        Returns:
            List of matching folder dictionaries

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> results = folders.search_folders("Production")
            >>> for folder in results:
            ...     print(f"{folder['DisplayName']}: {folder['FullyQualifiedName']}")
        """
        all_folders = self.folder_utils.list_all_folders(use_cache=True)

        search_lower = search_term.lower()
        results = []

        for folder in all_folders:
            display_name = folder.get('DisplayName', '').lower()
            description = folder.get('Description', '').lower()
            fully_qualified = folder.get('FullyQualifiedName', '').lower()

            if (search_lower in display_name or
                search_lower in description or
                search_lower in fully_qualified):
                results.append(folder)

        return results

    def get_folder_path(
        self,
        folder_key: str
    ) -> str:
        """Get fully qualified path for a folder.

        Args:
            folder_key: Folder GUID key

        Returns:
            Fully qualified folder path (e.g., "/Parent/Child")

        Example:
            >>> folders = FolderManagementExt(sdk)
            >>> path = folders.get_folder_path("5ebb73c3-...")
            >>> print(f"Folder path: {path}")
        """
        folder_info = self.folder_utils.get_folder_info(folder_key=folder_key)

        if not folder_info:
            return ""

        return folder_info.get('FullyQualifiedName', folder_info.get('DisplayName', ''))
