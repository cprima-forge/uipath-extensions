"""Job management operations.

Provides extended job operations beyond the official SDK's
retrieve, resume, and attachment methods.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class JobsExt:
    """Extensions for Job operations.

    The official SDK provides basic job retrieval and resume, but is missing:
    - Listing jobs with filtering and pagination
    - Stopping running jobs
    - Restarting failed jobs
    - Bulk job operations
    - Job statistics and aggregations

    This extension fills those gaps using the OData endpoints.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_jobs(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all jobs in a folder with optional filtering.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "State eq 'Successful'")
            top: Maximum number of results to return
            skip: Number of results to skip (for pagination)
            order_by: OData $orderby query (e.g., "StartTime desc")

        Returns:
            List of job dictionaries with State, StartTime, EndTime, etc.

        Raises:
            Exception: If API request fails

        Example:
            >>> jobs = JobsExt(sdk)
            >>> # List recent successful jobs
            >>> successful = jobs.list_jobs(
            ...     folder_key="5ebb73c3-...",
            ...     filter_query="State eq 'Successful'",
            ...     order_by="StartTime desc",
            ...     top=10
            ... )
            >>> for job in successful:
            ...     print(f"{job['Key']}: {job['Info']}")
            >>>
            >>> # List failed jobs from today
            >>> from datetime import datetime, UTC
            >>> today = datetime.now(UTC).strftime("%Y-%m-%d")
            >>> failed = jobs.list_jobs(
            ...     folder_key="5ebb73c3-...",
            ...     filter_query=f"State eq 'Faulted' and StartTime ge {today}T00:00:00Z"
            ... )
        """
        params = {}
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        if order_by:
            params["$orderby"] = order_by

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/Jobs",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_job(
        self,
        job_key: str,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get job details by key.

        Args:
            job_key: Job GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Job dictionary or None if not found

        Example:
            >>> jobs = JobsExt(sdk)
            >>> job = jobs.get_job(
            ...     job_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if job:
            ...     print(f"State: {job['State']}, Duration: {job['ExecutionDuration']}")
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            f"/odata/Jobs({job_key})",
            headers=headers
        )

        return response.json()

    def stop_job(
        self,
        job_key: str,
        folder_key: Optional[str] = None,
        strategy: str = "SoftStop"
    ) -> None:
        """Stop a running job.

        Args:
            job_key: Job GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)
            strategy: Stop strategy - "SoftStop" (graceful) or "Kill" (immediate)

        Raises:
            Exception: If API request fails or job not found

        Example:
            >>> jobs = JobsExt(sdk)
            >>> # Gracefully stop job
            >>> jobs.stop_job(
            ...     job_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-...",
            ...     strategy="SoftStop"
            ... )
            >>>
            >>> # Force kill job
            >>> jobs.stop_job(
            ...     job_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-...",
            ...     strategy="Kill"
            ... )
        """
        payload = {
            "jobId": job_key,
            "strategy": strategy
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "POST",
            "/odata/Jobs/UiPath.Server.Configuration.OData.StopJob",
            json=payload,
            headers=headers
        )

    def restart_job(
        self,
        job_key: str,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Restart a failed or stopped job.

        Args:
            job_key: Job GUID key
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            New job dictionary

        Raises:
            Exception: If API request fails or job cannot be restarted

        Example:
            >>> jobs = JobsExt(sdk)
            >>> new_job = jobs.restart_job(
            ...     job_key="a1b2c3d4-...",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Restarted as: {new_job['Key']}")
        """
        payload = {"jobId": job_key}

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/odata/Jobs/UiPath.Server.Configuration.OData.RestartJob",
            json=payload,
            headers=headers
        )

        return response.json()

    def bulk_stop_jobs(
        self,
        job_keys: List[str],
        folder_key: Optional[str] = None,
        strategy: str = "SoftStop"
    ) -> None:
        """Stop multiple jobs in bulk.

        Args:
            job_keys: List of job GUID keys
            folder_key: Folder GUID (optional - uses current folder if not specified)
            strategy: Stop strategy - "SoftStop" (graceful) or "Kill" (immediate)

        Raises:
            Exception: If API request fails

        Example:
            >>> jobs = JobsExt(sdk)
            >>> # Stop all running jobs for a process
            >>> running_jobs = jobs.list_jobs(
            ...     folder_key="5ebb73c3-...",
            ...     filter_query="State eq 'Running' and ProcessName eq 'MyProcess'"
            ... )
            >>> job_keys = [job['Key'] for job in running_jobs]
            >>> jobs.bulk_stop_jobs(
            ...     job_keys=job_keys,
            ...     folder_key="5ebb73c3-...",
            ...     strategy="SoftStop"
            ... )
        """
        for job_key in job_keys:
            try:
                self.stop_job(job_key, folder_key, strategy)
            except Exception as e:
                # Continue with other jobs even if one fails
                print(f"Failed to stop job {job_key}: {e}")

    def get_job_statistics(
        self,
        folder_key: Optional[str] = None,
        process_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get aggregated job statistics.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            process_name: Filter by process name (optional)
            start_date: Start date in ISO format (optional)
            end_date: End date in ISO format (optional)

        Returns:
            Dictionary with job counts by state

        Example:
            >>> jobs = JobsExt(sdk)
            >>> stats = jobs.get_job_statistics(
            ...     folder_key="5ebb73c3-...",
            ...     process_name="MyProcess"
            ... )
            >>> print(f"Successful: {stats['successful']}")
            >>> print(f"Failed: {stats['failed']}")
            >>> print(f"Total: {stats['total']}")
        """
        # Build filter query
        filters = []
        if process_name:
            filters.append(f"ProcessName eq '{process_name}'")
        if start_date:
            filters.append(f"StartTime ge {start_date}")
        if end_date:
            filters.append(f"StartTime le {end_date}")

        filter_query = " and ".join(filters) if filters else None

        # Get all jobs
        all_jobs = self.list_jobs(folder_key=folder_key, filter_query=filter_query)

        # Calculate statistics
        stats = {
            "total": len(all_jobs),
            "successful": 0,
            "failed": 0,
            "stopped": 0,
            "running": 0,
            "pending": 0,
            "suspended": 0,
            "by_state": {}
        }

        for job in all_jobs:
            state = job.get("State", "Unknown")
            stats["by_state"][state] = stats["by_state"].get(state, 0) + 1

            # Map to high-level categories
            if state == "Successful":
                stats["successful"] += 1
            elif state in ("Faulted", "Failed"):
                stats["failed"] += 1
            elif state in ("Stopped", "Stopping"):
                stats["stopped"] += 1
            elif state == "Running":
                stats["running"] += 1
            elif state == "Pending":
                stats["pending"] += 1
            elif state == "Suspended":
                stats["suspended"] += 1

        return stats

    def list_jobs_by_state(
        self,
        state: str,
        folder_key: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List jobs filtered by state.

        Args:
            state: Job state - "Successful", "Faulted", "Running", "Pending", "Stopped", "Suspended"
            folder_key: Folder GUID (optional - uses current folder if not specified)
            top: Maximum number of results (optional)

        Returns:
            List of job dictionaries

        Example:
            >>> jobs = JobsExt(sdk)
            >>> running = jobs.list_jobs_by_state(
            ...     state="Running",
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Currently running: {len(running)} jobs")
        """
        return self.list_jobs(
            folder_key=folder_key,
            filter_query=f"State eq '{state}'",
            top=top,
            order_by="StartTime desc"
        )

    def get_robot_jobs(
        self,
        robot_name: str,
        folder_key: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get jobs executed by a specific robot.

        Args:
            robot_name: Robot name
            folder_key: Folder GUID (optional - uses current folder if not specified)
            top: Maximum number of results (optional)

        Returns:
            List of job dictionaries

        Example:
            >>> jobs = JobsExt(sdk)
            >>> robot_jobs = jobs.get_robot_jobs(
            ...     robot_name="Robot01",
            ...     folder_key="5ebb73c3-...",
            ...     top=20
            ... )
        """
        return self.list_jobs(
            folder_key=folder_key,
            filter_query=f"Robot/Name eq '{robot_name}'",
            top=top,
            order_by="StartTime desc"
        )
