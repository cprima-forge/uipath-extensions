"""Process schedule management operations.

Provides CRUD operations for process schedules (cron-like triggers)
that are not available in the official SDK.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class SchedulesExt:
    """Extensions for Process Schedule operations.

    The official SDK does not provide schedule management. This extension
    adds full CRUD capabilities for process schedules using the OData endpoints.

    Schedules allow automated process execution on time-based triggers.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_process_schedules(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List all process schedules in a folder.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "Enabled eq true")
            top: Maximum number of results to return

        Returns:
            List of schedule dictionaries

        Raises:
            Exception: If API request fails

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> all_schedules = schedules.list_process_schedules(
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for schedule in all_schedules:
            ...     print(f"{schedule['Name']}: {schedule['CronExpression']}")
            >>>
            >>> # List only enabled schedules
            >>> enabled = schedules.list_process_schedules(
            ...     folder_key="5ebb73c3-...",
            ...     filter_query="Enabled eq true"
            ... )
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
            "/odata/ProcessSchedules",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_schedule(
        self,
        schedule_id: int,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get schedule details by ID.

        Args:
            schedule_id: Schedule ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Schedule dictionary or None if not found

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> schedule = schedules.get_schedule(
            ...     schedule_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if schedule:
            ...     print(f"Cron: {schedule['CronExpression']}")
            ...     print(f"Timezone: {schedule['TimeZoneId']}")
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            f"/odata/ProcessSchedules({schedule_id})",
            headers=headers
        )

        return response.json()

    def create_schedule(
        self,
        name: str,
        release_id: int,
        cron_expression: str,
        folder_key: Optional[str] = None,
        time_zone_id: str = "UTC",
        enabled: bool = True,
        execution_target: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new process schedule.

        Args:
            name: Schedule name
            release_id: Release ID to execute
            cron_expression: Cron expression (e.g., "0 9 * * 1-5" for 9 AM weekdays)
            folder_key: Folder GUID (optional - uses current folder if not specified)
            time_zone_id: Time zone ID (default: "UTC")
            enabled: Enable schedule immediately (default: True)
            execution_target: Execution target specification (optional)

        Returns:
            Created schedule dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> # Daily at 9 AM
            >>> daily = schedules.create_schedule(
            ...     name="DailyReport",
            ...     release_id=67890,
            ...     cron_expression="0 9 * * *",
            ...     folder_key="5ebb73c3-...",
            ...     time_zone_id="America/New_York"
            ... )
            >>>
            >>> # Weekdays at 8 AM
            >>> weekday = schedules.create_schedule(
            ...     name="WeekdayBackup",
            ...     release_id=67890,
            ...     cron_expression="0 8 * * 1-5",
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "Name": name,
            "ReleaseId": release_id,
            "CronExpression": cron_expression,
            "TimeZoneId": time_zone_id,
            "Enabled": enabled
        }

        if execution_target:
            payload["ExecutionTarget"] = execution_target

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/odata/ProcessSchedules",
            json=payload,
            headers=headers
        )

        return response.json()

    def update_schedule(
        self,
        schedule_id: int,
        folder_key: Optional[str] = None,
        name: Optional[str] = None,
        cron_expression: Optional[str] = None,
        time_zone_id: Optional[str] = None,
        enabled: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update an existing schedule.

        Args:
            schedule_id: Schedule ID
            folder_key: Folder GUID (optional - uses current folder if not specified)
            name: New name (optional)
            cron_expression: New cron expression (optional)
            time_zone_id: New time zone (optional)
            enabled: Enable/disable schedule (optional)

        Returns:
            Updated schedule dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> # Change to run every 2 hours
            >>> updated = schedules.update_schedule(
            ...     schedule_id=12345,
            ...     folder_key="5ebb73c3-...",
            ...     cron_expression="0 */2 * * *"
            ... )
        """
        payload = {}
        if name is not None:
            payload["Name"] = name
        if cron_expression is not None:
            payload["CronExpression"] = cron_expression
        if time_zone_id is not None:
            payload["TimeZoneId"] = time_zone_id
        if enabled is not None:
            payload["Enabled"] = enabled

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "PATCH",
            f"/odata/ProcessSchedules({schedule_id})",
            json=payload,
            headers=headers
        )

        return response.json()

    def delete_schedule(
        self,
        schedule_id: int,
        folder_key: Optional[str] = None
    ) -> None:
        """Delete a schedule.

        Args:
            schedule_id: Schedule ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> schedules.delete_schedule(
            ...     schedule_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "DELETE",
            f"/odata/ProcessSchedules({schedule_id})",
            headers=headers
        )

    def enable_schedule(
        self,
        schedule_id: int,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enable a schedule.

        Args:
            schedule_id: Schedule ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Updated schedule dictionary

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> schedules.enable_schedule(
            ...     schedule_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        return self.update_schedule(
            schedule_id=schedule_id,
            folder_key=folder_key,
            enabled=True
        )

    def disable_schedule(
        self,
        schedule_id: int,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Disable a schedule.

        Args:
            schedule_id: Schedule ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Updated schedule dictionary

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> schedules.disable_schedule(
            ...     schedule_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        return self.update_schedule(
            schedule_id=schedule_id,
            folder_key=folder_key,
            enabled=False
        )

    def get_schedules_for_release(
        self,
        release_id: int,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all schedules for a specific release.

        Args:
            release_id: Release ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of schedule dictionaries

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> release_schedules = schedules.get_schedules_for_release(
            ...     release_id=67890,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Found {len(release_schedules)} schedules for this release")
        """
        return self.list_process_schedules(
            folder_key=folder_key,
            filter_query=f"ReleaseId eq {release_id}"
        )

    def get_enabled_schedules(
        self,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all enabled schedules.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of enabled schedule dictionaries

        Example:
            >>> schedules = SchedulesExt(sdk)
            >>> active = schedules.get_enabled_schedules(
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for schedule in active:
            ...     print(f"{schedule['Name']}: next run at {schedule.get('NextRun')}")
        """
        return self.list_process_schedules(
            folder_key=folder_key,
            filter_query="Enabled eq true"
        )
