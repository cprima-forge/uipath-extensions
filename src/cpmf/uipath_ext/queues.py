"""Queue definition and management operations.

Provides CRUD operations for queue definitions and retention policies,
extending the official SDK's transaction-focused queue operations.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class QueuesExt:
    """Extensions for Queue Definition operations.

    The official SDK provides queue item transaction operations, but is missing:
    - CRUD for queue definitions
    - Queue retention policies
    - Queue statistics and metrics
    - Queue processing records
    - Queue configuration management

    This extension fills those gaps using the OData endpoints.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_queue_definitions(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List all queue definitions in a folder.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "Name eq 'MyQueue'")
            top: Maximum number of results to return

        Returns:
            List of queue definition dictionaries

        Raises:
            Exception: If API request fails

        Example:
            >>> queues = QueuesExt(sdk)
            >>> all_queues = queues.list_queue_definitions(
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for queue in all_queues:
            ...     print(f"{queue['Name']}: {queue['MaxNumberOfRetries']} retries")
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
            "/odata/QueueDefinitions",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_queue_definition(
        self,
        queue_name: str,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get queue definition by name.

        Args:
            queue_name: Queue name
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Queue definition dictionary or None if not found

        Example:
            >>> queues = QueuesExt(sdk)
            >>> queue = queues.get_queue_definition(
            ...     queue_name="TransactionQueue",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if queue:
            ...     print(f"Max retries: {queue['MaxNumberOfRetries']}")
            ...     print(f"Accept auto retry: {queue['AcceptAutomaticallyRetry']}")
        """
        queues = self.list_queue_definitions(
            folder_key=folder_key,
            filter_query=f"Name eq '{queue_name}'"
        )

        return queues[0] if queues else None

    def create_queue_definition(
        self,
        name: str,
        folder_key: Optional[str] = None,
        description: Optional[str] = None,
        max_retries: int = 0,
        accept_auto_retry: bool = False,
        enforce_unique_reference: bool = False
    ) -> Dict[str, Any]:
        """Create a new queue definition.

        Args:
            name: Queue name (must be unique in folder)
            folder_key: Folder GUID (optional - uses current folder if not specified)
            description: Queue description (optional)
            max_retries: Maximum number of retries for failed items (default: 0)
            accept_auto_retry: Accept automatic retry (default: False)
            enforce_unique_reference: Enforce unique reference (default: False)

        Returns:
            Created queue definition dictionary

        Raises:
            Exception: If API request fails or queue already exists

        Example:
            >>> queues = QueuesExt(sdk)
            >>> queue = queues.create_queue_definition(
            ...     name="OrderProcessing",
            ...     folder_key="5ebb73c3-...",
            ...     description="Queue for order processing workflow",
            ...     max_retries=3,
            ...     accept_auto_retry=True,
            ...     enforce_unique_reference=True
            ... )
            >>> print(f"Created queue: {queue['Name']} (ID: {queue['Id']})")
        """
        payload = {
            "Name": name,
            "MaxNumberOfRetries": max_retries,
            "AcceptAutomaticallyRetry": accept_auto_retry,
            "EnforceUniqueReference": enforce_unique_reference
        }

        if description:
            payload["Description"] = description

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/odata/QueueDefinitions",
            json=payload,
            headers=headers
        )

        return response.json()

    def update_queue_definition(
        self,
        queue_id: int,
        folder_key: Optional[str] = None,
        description: Optional[str] = None,
        max_retries: Optional[int] = None,
        accept_auto_retry: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update an existing queue definition.

        Args:
            queue_id: Queue definition ID
            folder_key: Folder GUID (optional - uses current folder if not specified)
            description: New description (optional)
            max_retries: New max retries (optional)
            accept_auto_retry: New auto retry setting (optional)

        Returns:
            Updated queue definition dictionary

        Raises:
            Exception: If API request fails or queue not found

        Example:
            >>> queues = QueuesExt(sdk)
            >>> updated = queues.update_queue_definition(
            ...     queue_id=12345,
            ...     folder_key="5ebb73c3-...",
            ...     max_retries=5
            ... )
        """
        payload = {}
        if description is not None:
            payload["Description"] = description
        if max_retries is not None:
            payload["MaxNumberOfRetries"] = max_retries
        if accept_auto_retry is not None:
            payload["AcceptAutomaticallyRetry"] = accept_auto_retry

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "PATCH",
            f"/odata/QueueDefinitions({queue_id})",
            json=payload,
            headers=headers
        )

        return response.json()

    def delete_queue_definition(
        self,
        queue_id: int,
        folder_key: Optional[str] = None
    ) -> None:
        """Delete a queue definition.

        Args:
            queue_id: Queue definition ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails or queue not found

        Example:
            >>> queues = QueuesExt(sdk)
            >>> queues.delete_queue_definition(
            ...     queue_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "DELETE",
            f"/odata/QueueDefinitions({queue_id})",
            headers=headers
        )

    def get_queue_statistics(
        self,
        queue_name: str,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get statistics for a queue.

        Retrieves counts of items by status.

        Args:
            queue_name: Queue name
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Dictionary with item counts by status

        Example:
            >>> queues = QueuesExt(sdk)
            >>> stats = queues.get_queue_statistics(
            ...     queue_name="OrderProcessing",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"New: {stats['new']}")
            >>> print(f"In Progress: {stats['in_progress']}")
            >>> print(f"Failed: {stats['failed']}")
            >>> print(f"Successful: {stats['successful']}")
        """
        # Get all items for this queue
        params = {
            "$filter": f"QueueDefinitionName eq '{queue_name}'"
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/QueueItems",
            params=params,
            headers=headers
        )

        items = response.json().get("value", [])

        # Calculate statistics
        stats = {
            "total": len(items),
            "new": 0,
            "in_progress": 0,
            "failed": 0,
            "successful": 0,
            "retried": 0,
            "deleted": 0,
            "by_status": {}
        }

        for item in items:
            status = item.get("Status", "Unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

            # Map to high-level categories
            if status == "New":
                stats["new"] += 1
            elif status == "InProgress":
                stats["in_progress"] += 1
            elif status == "Failed":
                stats["failed"] += 1
            elif status == "Successful":
                stats["successful"] += 1
            elif status == "Retried":
                stats["retried"] += 1
            elif status == "Deleted":
                stats["deleted"] += 1

        return stats

    def set_retention_policy(
        self,
        queue_id: int,
        retention_days: int,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Set retention policy for a queue.

        Args:
            queue_id: Queue definition ID
            retention_days: Number of days to retain completed items
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Retention policy dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> queues = QueuesExt(sdk)
            >>> policy = queues.set_retention_policy(
            ...     queue_id=12345,
            ...     retention_days=30,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "QueueDefinitionId": queue_id,
            "RetentionDays": retention_days
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/odata/QueueRetention",
            json=payload,
            headers=headers
        )

        return response.json()

    def get_retention_policy(
        self,
        queue_id: int,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get retention policy for a queue.

        Args:
            queue_id: Queue definition ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Retention policy dictionary or None if not set

        Example:
            >>> queues = QueuesExt(sdk)
            >>> policy = queues.get_retention_policy(
            ...     queue_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if policy:
            ...     print(f"Retention: {policy['RetentionDays']} days")
        """
        params = {
            "$filter": f"QueueDefinitionId eq {queue_id}"
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/QueueRetention",
            params=params,
            headers=headers
        )

        policies = response.json().get("value", [])
        return policies[0] if policies else None

    def get_processing_records(
        self,
        queue_id: int,
        folder_key: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get processing records for a queue.

        Args:
            queue_id: Queue definition ID
            folder_key: Folder GUID (optional - uses current folder if not specified)
            top: Maximum number of results (optional)

        Returns:
            List of processing record dictionaries

        Example:
            >>> queues = QueuesExt(sdk)
            >>> records = queues.get_processing_records(
            ...     queue_id=12345,
            ...     folder_key="5ebb73c3-...",
            ...     top=100
            ... )
            >>> for record in records:
            ...     print(f"Item: {record['QueueItemId']}, Status: {record['Status']}")
        """
        params = {
            "$filter": f"QueueDefinitionId eq {queue_id}"
        }
        if top:
            params["$top"] = top

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/QueueProcessingRecords",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])
