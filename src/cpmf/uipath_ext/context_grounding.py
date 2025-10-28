"""Context Grounding extensions for enhanced storage visibility.

Provides high-level operations for Context Grounding that aren't available
in the official SDK, particularly around storage bucket inspection and
ingestion verification.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath

from .buckets import BucketExtensions
from .folder_utils import FolderUtils
from ._internal.helpers import get_bucket_id_from_index, get_folder_id_from_api


class ContextGroundingExt:
    """Extensions for Context Grounding operations.

    Provides enhanced capabilities for:
    - Listing files in Context Grounding storage buckets
    - Verifying file ingestion status
    - Checking ingestion metrics
    - Inspecting bucket configuration

    Example:
        >>> from uipath import UiPath
        >>> from uipath_sdk_extensions import ContextGroundingExt
        >>>
        >>> sdk = UiPath()
        >>> cg = ContextGroundingExt(sdk)
        >>>
        >>> # List all files in index storage
        >>> files = cg.list_bucket_files(
        ...     index_name="MyIndex",
        ...     folder_key="5ebb73c3-b114-43b2-8615-c6a093e0eaab"
        ... )
        >>> print(f"Found {len(files)} files")
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk
        self.buckets = BucketExtensions(sdk)
        self.folders = FolderUtils(sdk)

    def list_bucket_files(
        self,
        index_name: str,
        folder_key: str,
        directory: str = "/",
        recursive: bool = True,
        file_name_glob: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all files in the Context Grounding storage bucket.

        This is the most commonly needed operation - seeing what files
        are actually stored in the bucket associated with a Context Grounding index.

        Args:
            index_name: Name of the Context Grounding index
            folder_key: Folder GUID where the index exists
            directory: Root directory to list (default: "/" for all)
            recursive: Include subdirectories (default: True)
            file_name_glob: Optional file filter (e.g., "*.pdf")

        Returns:
            List of file dictionaries with FullPath, Size, ContentType, IsDirectory

        Raises:
            ValueError: If index or folder not found
            Exception: If API request fails

        Example:
            >>> files = cg.list_bucket_files(
            ...     index_name="CntxtGrdngAiTrustLayer_2025-04",
            ...     folder_key="5ebb73c3-b114-43b2-8615-c6a093e0eaab",
            ...     recursive=True
            ... )
            >>> for f in files:
            ...     if not f['IsDirectory']:
            ...         print(f"{f['FullPath']}: {f['Size']/1024:.1f} KB")
        """
        # Get bucket and folder IDs
        bucket_id = get_bucket_id_from_index(self.sdk, index_name, folder_key)
        if not bucket_id:
            raise ValueError(f"Could not find bucket for index: {index_name}")

        folder_id = get_folder_id_from_api(self.sdk, folder_key)
        if not folder_id:
            raise ValueError(f"Folder not found: {folder_key}")

        # List files using bucket extensions
        return self.buckets.list_files(
            bucket_id=bucket_id,
            folder_id=folder_id,
            directory=directory,
            recursive=recursive,
            file_name_glob=file_name_glob
        )

    def get_ingestion_status(self, index_name: str, folder_key: str) -> Dict[str, Any]:
        """Get detailed ingestion status for an index.

        Returns enhanced status information including:
        - Last ingestion status (Successful, Failed, etc.)
        - Whether ingestion is currently in progress
        - Last ingestion timestamp
        - Memory and disk usage

        Args:
            index_name: Name of the Context Grounding index
            folder_key: Folder GUID where the index exists

        Returns:
            Dictionary with status information

        Example:
            >>> status = cg.get_ingestion_status(
            ...     index_name="MyIndex",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Status: {status['last_ingestion_status']}")
            >>> print(f"In Progress: {status['in_progress']}")
            >>> print(f"Last Ingested: {status['last_ingested']}")
        """
        index = self.sdk.context_grounding.retrieve(
            name=index_name,
            folder_key=folder_key
        )

        return {
            "last_ingestion_status": getattr(index, "last_ingestion_status", "unknown"),
            "in_progress": index.in_progress_ingestion() if hasattr(index, "in_progress_ingestion") else False,
            "last_ingested": getattr(index, "last_ingested", None),
            "last_queried": getattr(index, "last_queried", None),
            "memory_usage": getattr(index, "memory_usage", 0),
            "disk_usage": getattr(index, "disk_usage", 0),
        }

    def verify_file_indexed(
        self,
        index_name: str,
        folder_key: str,
        file_path: str
    ) -> bool:
        """Check if a specific file exists in the storage bucket.

        Note: This checks if the file is in storage, not necessarily if it
        was successfully indexed during ingestion. Files can exist in storage
        but be skipped during ingestion if they don't match the data source
        directoryPath configuration.

        Args:
            index_name: Name of the Context Grounding index
            folder_key: Folder GUID where the index exists
            file_path: Full path of the file to check (e.g., "/documents/file.pdf")

        Returns:
            True if file exists in storage bucket, False otherwise

        Example:
            >>> exists = cg.verify_file_indexed(
            ...     index_name="MyIndex",
            ...     folder_key="5ebb73c3-...",
            ...     file_path="/Ferrotoroid_memory_crystals.pdf"
            ... )
            >>> if exists:
            ...     print("File is in storage")
        """
        files = self.list_bucket_files(index_name, folder_key, recursive=True)

        for file in files:
            if file.get("FullPath") == file_path or file.get("FullPath") == file_path.lstrip("/"):
                return True

        return False

    def get_bucket_file_stats(
        self,
        index_name: str,
        folder_key: str
    ) -> Dict[str, Any]:
        """Get statistics about files in the storage bucket.

        Provides summary information useful for debugging ingestion issues.

        Args:
            index_name: Name of the Context Grounding index
            folder_key: Folder GUID where the index exists

        Returns:
            Dictionary with file statistics

        Example:
            >>> stats = cg.get_bucket_file_stats("MyIndex", "5ebb73c3-...")
            >>> print(f"Total files: {stats['total_files']}")
            >>> print(f"Total size: {stats['total_size_mb']:.1f} MB")
            >>> print(f"By directory: {stats['files_by_directory']}")
        """
        files = self.list_bucket_files(index_name, folder_key, recursive=True)

        # Filter out directories
        actual_files = [f for f in files if not f.get("IsDirectory", False)]

        # Calculate statistics
        total_size = sum(f.get("Size", 0) for f in actual_files)

        # Group by directory
        by_directory = self.buckets.organize_files_by_directory(actual_files)

        # Group by content type
        by_content_type: Dict[str, int] = {}
        for f in actual_files:
            content_type = f.get("ContentType", "unknown")
            by_content_type[content_type] = by_content_type.get(content_type, 0) + 1

        return {
            "total_files": len(actual_files),
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "files_by_directory": {k: len(v) for k, v in by_directory.items()},
            "files_by_content_type": by_content_type,
            "directories": sorted(by_directory.keys()),
        }

    def get_data_source_config(self, index_name: str, folder_key: str) -> Dict[str, Any]:
        """Get the data source configuration for an index.

        Returns information about what files the index is configured to ingest,
        which is crucial for understanding why some files might be skipped.

        Args:
            index_name: Name of the Context Grounding index
            folder_key: Folder GUID where the index exists

        Returns:
            Dictionary with data source configuration

        Example:
            >>> config = cg.get_data_source_config("MyIndex", "5ebb73c3-...")
            >>> print(f"Watches: {config['directoryPath']}{config['fileNameGlob']}")
            >>> print(f"Bucket: {config['bucketName']}")
        """
        index = self.sdk.context_grounding.retrieve(
            name=index_name,
            folder_key=folder_key
        )

        datasource = index.data_source

        return {
            "bucketName": getattr(datasource, "bucketName", None),
            "directoryPath": getattr(datasource, "directoryPath", "/"),
            "fileNameGlob": getattr(datasource, "fileNameGlob", "*"),
            "type": getattr(datasource, "@odata.type", None),
        }
