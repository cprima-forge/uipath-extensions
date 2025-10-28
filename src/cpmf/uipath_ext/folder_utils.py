"""Folder navigation and ID/Key conversion utilities.

Provides helpers for converting between folder GUIDs and numeric IDs,
and listing accessible folders.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class FolderUtils:
    """Utilities for folder operations and ID/Key conversions.

    The UiPath API uses different identifiers in different contexts:
    - Folder Key (GUID): Used in Context Grounding and some OData endpoints
    - Folder ID (numeric): Used in bucket operations and OrganizationUnitId headers

    This class provides conversion utilities and folder listing.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk
        self._folder_cache: Optional[List[Dict[str, Any]]] = None

    def list_all_folders(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """List all folders accessible to the current user.

        Args:
            use_cache: Use cached folder list if available (default: True)

        Returns:
            List of folder dictionaries with Id, Key, DisplayName, etc.

        Raises:
            Exception: If API request fails
        """
        if use_cache and self._folder_cache is not None:
            return self._folder_cache

        response = self.sdk.api_client.request("GET", "/odata/Folders")
        folders = response.json().get("value", [])

        if use_cache:
            self._folder_cache = folders

        return folders

    def get_folder_id_from_key(self, folder_key: str) -> Optional[int]:
        """Convert folder GUID key to numeric ID.

        Args:
            folder_key: Folder GUID (e.g., "5ebb73c3-b114-43b2-8615-c6a093e0eaab")

        Returns:
            Numeric folder ID (e.g., 5083200), or None if not found

        Example:
            >>> utils = FolderUtils(sdk)
            >>> folder_id = utils.get_folder_id_from_key("5ebb73c3-...")
            >>> print(folder_id)
            5083200
        """
        folders = self.list_all_folders()

        for folder in folders:
            if folder.get("Key") == folder_key:
                return folder.get("Id")

        return None

    def get_folder_key_from_id(self, folder_id: int) -> Optional[str]:
        """Convert numeric folder ID to GUID key.

        Args:
            folder_id: Numeric folder ID (e.g., 5083200)

        Returns:
            Folder GUID key, or None if not found

        Example:
            >>> utils = FolderUtils(sdk)
            >>> folder_key = utils.get_folder_key_from_id(5083200)
            >>> print(folder_key)
            "5ebb73c3-b114-43b2-8615-c6a093e0eaab"
        """
        folders = self.list_all_folders()

        for folder in folders:
            if folder.get("Id") == folder_id:
                return folder.get("Key")

        return None

    def get_folder_info(self, folder_key: Optional[str] = None, folder_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get complete folder information by key or ID.

        Args:
            folder_key: Folder GUID key (optional)
            folder_id: Numeric folder ID (optional)

        Returns:
            Folder dictionary with all attributes, or None if not found

        Raises:
            ValueError: If neither folder_key nor folder_id provided

        Example:
            >>> utils = FolderUtils(sdk)
            >>> info = utils.get_folder_info(folder_key="5ebb73c3-...")
            >>> print(f"{info['DisplayName']}: {info['FullyQualifiedName']}")
        """
        if not folder_key and not folder_id:
            raise ValueError("Must provide either folder_key or folder_id")

        folders = self.list_all_folders()

        for folder in folders:
            if folder_key and folder.get("Key") == folder_key:
                return folder
            if folder_id and folder.get("Id") == folder_id:
                return folder

        return None

    def clear_cache(self) -> None:
        """Clear the internal folder cache.

        Call this after folder changes to force re-fetching on next request.
        """
        self._folder_cache = None
