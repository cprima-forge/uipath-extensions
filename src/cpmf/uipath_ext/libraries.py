"""Library package management operations.

Provides operations for managing reusable library packages
that are not available in the official SDK.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class LibrariesExt:
    """Extensions for Library package operations.

    The official SDK does not provide library management. This extension
    adds capabilities for listing, retrieving, and managing library packages.

    Libraries are reusable package components that can be shared across processes.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_libraries(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all libraries in a folder.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "Title eq 'MyLibrary'")
            top: Maximum number of results to return
            order_by: OData $orderby query (e.g., "Published desc")

        Returns:
            List of library dictionaries

        Raises:
            Exception: If API request fails

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> all_libs = libraries.list_libraries(
            ...     folder_key="5ebb73c3-...",
            ...     order_by="Published desc"
            ... )
            >>> for lib in all_libs:
            ...     print(f"{lib['Title']} v{lib['Version']}")
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
            "/odata/Libraries",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_library(
        self,
        library_id: str,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get library details by ID.

        Args:
            library_id: Library ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Library dictionary or None if not found

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> lib = libraries.get_library(
            ...     library_id="MyLibrary",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if lib:
            ...     print(f"Version: {lib['Version']}")
            ...     print(f"Description: {lib['Description']}")
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            f"/odata/Libraries('{library_id}')",
            headers=headers
        )

        return response.json()

    def get_library_by_title(
        self,
        title: str,
        folder_key: Optional[str] = None,
        version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get library by title and optional version.

        Args:
            title: Library title
            folder_key: Folder GUID (optional - uses current folder if not specified)
            version: Library version (optional - gets latest if not specified)

        Returns:
            Library dictionary or None if not found

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> # Get latest version
            >>> latest = libraries.get_library_by_title(
            ...     title="CommonUtilities",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>>
            >>> # Get specific version
            >>> v1 = libraries.get_library_by_title(
            ...     title="CommonUtilities",
            ...     folder_key="5ebb73c3-...",
            ...     version="1.0.5"
            ... )
        """
        filter_query = f"Title eq '{title}'"
        if version:
            filter_query += f" and Version eq '{version}'"

        libraries = self.list_libraries(
            folder_key=folder_key,
            filter_query=filter_query,
            order_by="Published desc",
            top=1
        )

        return libraries[0] if libraries else None

    def list_library_versions(
        self,
        title: str,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all versions of a library.

        Args:
            title: Library title
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of library dictionaries ordered by version descending

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> versions = libraries.list_library_versions(
            ...     title="CommonUtilities",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for lib in versions:
            ...     print(f"v{lib['Version']}: {lib['Published']}")
        """
        return self.list_libraries(
            folder_key=folder_key,
            filter_query=f"Title eq '{title}'",
            order_by="Version desc"
        )

    def delete_library_version(
        self,
        library_id: str,
        folder_key: Optional[str] = None
    ) -> None:
        """Delete a specific library version.

        Args:
            library_id: Library ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> libraries.delete_library_version(
            ...     library_id="MyLibrary",
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "DELETE",
            f"/odata/Libraries('{library_id}')",
            headers=headers
        )

    def get_library_dependencies(
        self,
        library_id: str,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get dependencies for a library.

        Args:
            library_id: Library ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of dependency dictionaries

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> deps = libraries.get_library_dependencies(
            ...     library_id="MyLibrary",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for dep in deps:
            ...     print(f"Depends on: {dep.get('Id')} v{dep.get('Version')}")
        """
        library = self.get_library(library_id, folder_key)

        if not library:
            return []

        # Dependencies are typically in the library metadata
        return library.get("Dependencies", [])

    def search_libraries(
        self,
        search_term: str,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search libraries by title or description.

        Args:
            search_term: Search term
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of matching library dictionaries

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> results = libraries.search_libraries(
            ...     search_term="utilities",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for lib in results:
            ...     print(f"{lib['Title']}: {lib['Description']}")
        """
        filter_query = f"contains(Title, '{search_term}') or contains(Description, '{search_term}')"

        return self.list_libraries(
            folder_key=folder_key,
            filter_query=filter_query,
            order_by="Published desc"
        )

    def get_latest_versions(
        self,
        folder_key: Optional[str] = None,
        top: int = 10
    ) -> List[Dict[str, Any]]:
        """Get latest published library versions.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            top: Maximum number of results (default: 10)

        Returns:
            List of library dictionaries

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> recent = libraries.get_latest_versions(
            ...     folder_key="5ebb73c3-...",
            ...     top=5
            ... )
            >>> for lib in recent:
            ...     print(f"{lib['Title']} v{lib['Version']} - {lib['Published']}")
        """
        return self.list_libraries(
            folder_key=folder_key,
            order_by="Published desc",
            top=top
        )

    def get_library_usage(
        self,
        library_title: str,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get usage statistics for a library.

        Note: This provides basic version information. For detailed usage
        tracking (which processes use this library), you would need to
        query releases and examine their dependencies.

        Args:
            library_title: Library title
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Dictionary with version count and latest version info

        Example:
            >>> libraries = LibrariesExt(sdk)
            >>> usage = libraries.get_library_usage(
            ...     library_title="CommonUtilities",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Total versions: {usage['version_count']}")
            >>> print(f"Latest: v{usage['latest_version']}")
        """
        versions = self.list_library_versions(library_title, folder_key)

        if not versions:
            return {
                "library_title": library_title,
                "version_count": 0,
                "latest_version": None,
                "versions": []
            }

        return {
            "library_title": library_title,
            "version_count": len(versions),
            "latest_version": versions[0].get("Version"),
            "latest_published": versions[0].get("Published"),
            "versions": [v.get("Version") for v in versions]
        }
