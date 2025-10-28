"""Storage bucket operations and file listing.

Provides direct access to storage bucket operations that aren't
exposed by the official SDK, including file listing with subdirectory support.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath

from ._internal.helpers import get_folder_id_from_api, make_bucket_request


class BucketExtensions:
    """Extensions for storage bucket operations.

    Uses the OData endpoint documented in swagger.v20.0.json:
    /odata/Buckets({key})/UiPath.Server.Configuration.OData.GetFiles

    Alternative REST API endpoint also available:
    /api/Buckets/{id}/ListFiles (with continuation token support)
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_files(
        self,
        bucket_id: int,
        folder_id: int,
        directory: str = "/",
        recursive: bool = True,
        file_name_glob: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List files in a storage bucket.

        Args:
            bucket_id: Numeric bucket ID
            folder_id: Numeric folder/organization unit ID
            directory: Directory path to list (default: "/")
            recursive: Include subdirectories in flat view (default: True)
            file_name_glob: Optional file filter pattern (e.g., "*.pdf")

        Returns:
            List of file dictionaries with FullPath, Size, ContentType, IsDirectory

        Raises:
            Exception: If API request fails

        Example:
            >>> buckets = BucketExtensions(sdk)
            >>> files = buckets.list_files(
            ...     bucket_id=140055,
            ...     folder_id=5083200,
            ...     recursive=True
            ... )
            >>> for f in files:
            ...     print(f"{f['FullPath']}: {f['Size']/1024:.1f} KB")
        """
        params = {
            "directory": directory,
            "recursive": str(recursive).lower()
        }

        if file_name_glob:
            params["fileNameGlob"] = file_name_glob

        response = make_bucket_request(
            self.sdk,
            "GET",
            f"/orchestrator_/odata/Buckets({bucket_id})/UiPath.Server.Configuration.OData.GetFiles",
            folder_id,
            params=params
        )

        data = response.json()
        return data.get("value", [])

    def get_bucket_info(self, bucket_id: int, folder_id: int) -> Optional[Dict[str, Any]]:
        """Get bucket metadata and configuration.

        Args:
            bucket_id: Numeric bucket ID
            folder_id: Numeric folder/organization unit ID

        Returns:
            Bucket dictionary with Id, Name, Description, etc., or None if not found

        Raises:
            Exception: If API request fails
        """
        response = make_bucket_request(
            self.sdk,
            "GET",
            "/odata/Buckets",
            folder_id
        )

        buckets = response.json().get("value", [])

        for bucket in buckets:
            if bucket.get("Id") == bucket_id:
                return bucket

        return None

    def list_all_buckets(self, folder_id: int) -> List[Dict[str, Any]]:
        """List all storage buckets in a folder.

        Args:
            folder_id: Numeric folder/organization unit ID

        Returns:
            List of bucket dictionaries

        Raises:
            Exception: If API request fails
        """
        response = make_bucket_request(
            self.sdk,
            "GET",
            "/odata/Buckets",
            folder_id
        )

        return response.json().get("value", [])

    def organize_files_by_directory(self, files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Organize flat file list into directory structure.

        Helper method to group files by their parent directory.

        Args:
            files: List of file dictionaries from list_files()

        Returns:
            Dictionary mapping directory paths to lists of files

        Example:
            >>> files = buckets.list_files(bucket_id, folder_id, recursive=True)
            >>> by_dir = buckets.organize_files_by_directory(files)
            >>> for dir_path, dir_files in by_dir.items():
            ...     print(f"{dir_path}/: {len(dir_files)} files")
        """
        result: Dict[str, List[Dict[str, Any]]] = {}

        for file in files:
            full_path = file.get("FullPath", "")

            if "/" in full_path:
                dir_path = full_path.rsplit("/", 1)[0]
            else:
                dir_path = "/"  # Root directory

            if dir_path not in result:
                result[dir_path] = []

            result[dir_path].append(file)

        return result
