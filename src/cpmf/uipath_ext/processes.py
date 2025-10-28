"""Process and release management operations.

Provides extended operations for processes and releases beyond the
official SDK's basic execution capabilities.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class ProcessesExt:
    """Extensions for Process and Release operations.

    The official SDK provides basic process execution, but is missing:
    - Listing releases and versions
    - Release retention policies
    - Cross-folder release operations
    - Release metadata and configuration

    This extension fills those gaps using the OData endpoints.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_releases(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all releases in a folder.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "ProcessKey eq 'MyProcess'")
            top: Maximum number of results to return
            order_by: OData $orderby query (e.g., "Published desc")

        Returns:
            List of release dictionaries

        Raises:
            Exception: If API request fails

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> releases = processes.list_releases(
            ...     folder_key="5ebb73c3-...",
            ...     order_by="Published desc",
            ...     top=10
            ... )
            >>> for release in releases:
            ...     print(f"{release['Name']} v{release['ProcessVersion']}")
        """
        params = {}
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top
        if order_by:
            params["$orderby"] = order_by

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/Releases",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_release(
        self,
        release_key: str,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get release details by key.

        Args:
            release_key: Release GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Release dictionary or None if not found

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> release = processes.get_release(
            ...     release_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if release:
            ...     print(f"Process: {release['ProcessKey']}, Version: {release['ProcessVersion']}")
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            f"/odata/Releases({release_key})",
            headers=headers
        )

        return response.json()

    def get_release_by_process_name(
        self,
        process_name: str,
        folder_key: Optional[str] = None,
        version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get release by process name and optional version.

        Args:
            process_name: Process name (e.g., "MyProcess")
            folder_key: Folder GUID (optional - uses current folder if not specified)
            version: Process version (optional - gets latest if not specified)

        Returns:
            Release dictionary or None if not found

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> # Get latest version
            >>> latest = processes.get_release_by_process_name(
            ...     process_name="OrderProcessing",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>>
            >>> # Get specific version
            >>> v2 = processes.get_release_by_process_name(
            ...     process_name="OrderProcessing",
            ...     folder_key="5ebb73c3-...",
            ...     version="2.0.0"
            ... )
        """
        filter_query = f"ProcessKey eq '{process_name}'"
        if version:
            filter_query += f" and ProcessVersion eq '{version}'"

        releases = self.list_releases(
            folder_key=folder_key,
            filter_query=filter_query,
            order_by="Published desc",
            top=1
        )

        return releases[0] if releases else None

    def list_process_versions(
        self,
        process_name: str,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all versions of a process.

        Args:
            process_name: Process name
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of release dictionaries ordered by version descending

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> versions = processes.list_process_versions(
            ...     process_name="OrderProcessing",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for release in versions:
            ...     print(f"v{release['ProcessVersion']}: {release['Published']}")
        """
        return self.list_releases(
            folder_key=folder_key,
            filter_query=f"ProcessKey eq '{process_name}'",
            order_by="ProcessVersion desc"
        )

    def list_processes(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List all processes in a folder.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (optional)
            top: Maximum number of results to return

        Returns:
            List of process dictionaries

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> all_processes = processes.list_processes(
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for process in all_processes:
            ...     print(f"{process['Key']}: {process['Description']}")
        """
        params = {}
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/Processes",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_process(
        self,
        process_key: str,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get process details by key.

        Args:
            process_key: Process key (name)
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Process dictionary or None if not found

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> process = processes.get_process(
            ...     process_key="OrderProcessing",
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            f"/odata/Processes('{process_key}')",
            headers=headers
        )

        return response.json()

    def set_retention_policy(
        self,
        release_id: int,
        retention_days: int,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Set retention policy for a release.

        Args:
            release_id: Release ID
            retention_days: Number of days to retain release data
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Retention policy dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> policy = processes.set_retention_policy(
            ...     release_id=12345,
            ...     retention_days=90,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "ReleaseId": release_id,
            "RetentionDays": retention_days
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/odata/ReleaseRetention",
            json=payload,
            headers=headers
        )

        return response.json()

    def get_retention_policy(
        self,
        release_id: int,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get retention policy for a release.

        Args:
            release_id: Release ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Retention policy dictionary or None if not set

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> policy = processes.get_retention_policy(
            ...     release_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if policy:
            ...     print(f"Retention: {policy['RetentionDays']} days")
        """
        params = {
            "$filter": f"ReleaseId eq {release_id}"
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/ReleaseRetention",
            params=params,
            headers=headers
        )

        policies = response.json().get("value", [])
        return policies[0] if policies else None

    def update_release(
        self,
        release_key: str,
        folder_key: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        auto_update: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update release metadata.

        Args:
            release_key: Release GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)
            name: New release name (optional)
            description: New description (optional)
            auto_update: Enable/disable auto-update (optional)

        Returns:
            Updated release dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> updated = processes.update_release(
            ...     release_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-...",
            ...     description="Updated production release",
            ...     auto_update=True
            ... )
        """
        payload = {}
        if name is not None:
            payload["Name"] = name
        if description is not None:
            payload["Description"] = description
        if auto_update is not None:
            payload["AutoUpdate"] = auto_update

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "PATCH",
            f"/odata/Releases({release_key})",
            json=payload,
            headers=headers
        )

        return response.json()

    def delete_release(
        self,
        release_key: str,
        folder_key: Optional[str] = None
    ) -> None:
        """Delete a release.

        Args:
            release_key: Release GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails

        Example:
            >>> processes = ProcessesExt(sdk)
            >>> processes.delete_release(
            ...     release_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "DELETE",
            f"/odata/Releases({release_key})",
            headers=headers
        )
