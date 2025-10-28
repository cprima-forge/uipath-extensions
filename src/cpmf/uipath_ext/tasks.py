"""Task and form management operations (Human-in-the-Loop).

Provides operations for creating, managing, and completing tasks with forms
that are not available in the official SDK.
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class TasksExt:
    """Extensions for Task and Form operations.

    The official SDK does not provide task management. This extension
    adds capabilities for human-in-the-loop workflows, form tasks,
    and task approval processes.

    Tasks allow human interaction in automated processes for approvals,
    data validation, exception handling, etc.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_tasks(
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all tasks in a folder.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "Status eq 'Unassigned'")
            top: Maximum number of results to return
            order_by: OData $orderby query (e.g., "CreationTime desc")

        Returns:
            List of task dictionaries

        Raises:
            Exception: If API request fails

        Example:
            >>> tasks = TasksExt(sdk)
            >>> all_tasks = tasks.list_tasks(
            ...     folder_key="5ebb73c3-...",
            ...     order_by="CreationTime desc"
            ... )
            >>> for task in all_tasks:
            ...     print(f"{task['Title']}: {task['Status']}")
            >>>
            >>> # List pending tasks
            >>> pending = tasks.list_tasks(
            ...     folder_key="5ebb73c3-...",
            ...     filter_query="Status eq 'Unassigned' or Status eq 'Pending'"
            ... )
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
            "/odata/Tasks",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])

    def get_task(
        self,
        task_id: int,
        folder_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get task details by ID.

        Args:
            task_id: Task ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Task dictionary or None if not found

        Example:
            >>> tasks = TasksExt(sdk)
            >>> task = tasks.get_task(
            ...     task_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> if task:
            ...     print(f"Title: {task['Title']}")
            ...     print(f"Assigned to: {task.get('AssignedToUser')}")
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            f"/odata/Tasks({task_id})",
            headers=headers
        )

        return response.json()

    def create_task(
        self,
        title: str,
        task_catalog_id: int,
        folder_key: Optional[str] = None,
        priority: str = "Medium",
        assigned_to_user: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new task.

        Args:
            title: Task title
            task_catalog_id: Task catalog ID (defines the task type/form)
            folder_key: Folder GUID (optional - uses current folder if not specified)
            priority: Task priority - "Low", "Medium", "High", "Critical" (default: "Medium")
            assigned_to_user: User ID to assign task to (optional)
            data: Task data/form data (optional)

        Returns:
            Created task dictionary

        Raises:
            Exception: If API request fails

        Example:
            >>> tasks = TasksExt(sdk)
            >>> task = tasks.create_task(
            ...     title="Approve Purchase Order #1234",
            ...     task_catalog_id=56789,
            ...     folder_key="5ebb73c3-...",
            ...     priority="High",
            ...     data={"OrderNumber": "1234", "Amount": 5000}
            ... )
            >>> print(f"Created task ID: {task['Id']}")
        """
        payload = {
            "title": title,
            "catalogId": task_catalog_id,
            "priority": priority
        }

        if assigned_to_user:
            payload["userId"] = assigned_to_user
        if data:
            payload["data"] = data

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "POST",
            "/forms/TaskForms/CreateFormTask",
            json=payload,
            headers=headers
        )

        return response.json()

    def complete_task(
        self,
        task_id: int,
        action: str,
        folder_key: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        comment: Optional[str] = None
    ) -> None:
        """Complete a task with an action.

        Args:
            task_id: Task ID
            action: Action name (e.g., "Approve", "Reject", "Submit")
            folder_key: Folder GUID (optional - uses current folder if not specified)
            data: Updated task data (optional)
            comment: Completion comment (optional)

        Raises:
            Exception: If API request fails

        Example:
            >>> tasks = TasksExt(sdk)
            >>> # Approve task
            >>> tasks.complete_task(
            ...     task_id=12345,
            ...     action="Approve",
            ...     folder_key="5ebb73c3-...",
            ...     comment="Approved by manager"
            ... )
            >>>
            >>> # Reject with reason
            >>> tasks.complete_task(
            ...     task_id=12345,
            ...     action="Reject",
            ...     folder_key="5ebb73c3-...",
            ...     data={"RejectionReason": "Insufficient budget"},
            ...     comment="Budget exceeded"
            ... )
        """
        payload = {
            "taskId": task_id,
            "actionName": action
        }

        if data:
            payload["data"] = data
        if comment:
            payload["comment"] = comment

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "POST",
            "/forms/TaskForms/CompleteTask",
            json=payload,
            headers=headers
        )

    def save_task_data(
        self,
        task_id: int,
        data: Dict[str, Any],
        folder_key: Optional[str] = None
    ) -> None:
        """Save task data without completing the task (draft save).

        Args:
            task_id: Task ID
            data: Task data to save
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails

        Example:
            >>> tasks = TasksExt(sdk)
            >>> # Save partial progress
            >>> tasks.save_task_data(
            ...     task_id=12345,
            ...     folder_key="5ebb73c3-...",
            ...     data={"Field1": "Value1", "Field2": "In Progress"}
            ... )
        """
        payload = {
            "taskId": task_id,
            "data": data
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "POST",
            "/forms/TaskForms/SaveTaskData",
            json=payload,
            headers=headers
        )

    def reassign_task(
        self,
        task_id: int,
        user_id: int,
        folder_key: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Reassign task to a different user.

        Args:
            task_id: Task ID
            user_id: New user ID to assign to
            folder_key: Folder GUID (optional - uses current folder if not specified)
            data: Updated task data (optional)

        Raises:
            Exception: If API request fails

        Example:
            >>> tasks = TasksExt(sdk)
            >>> tasks.reassign_task(
            ...     task_id=12345,
            ...     user_id=67890,
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "taskId": task_id,
            "userId": user_id
        }

        if data:
            payload["data"] = data

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "POST",
            "/forms/TaskForms/SaveAndReassignTask",
            json=payload,
            headers=headers
        )

    def bulk_complete_tasks(
        self,
        task_ids: List[int],
        action: str,
        folder_key: Optional[str] = None
    ) -> None:
        """Complete multiple tasks with the same action.

        Args:
            task_ids: List of task IDs
            action: Action name (e.g., "Approve", "Reject")
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Raises:
            Exception: If API request fails

        Example:
            >>> tasks = TasksExt(sdk)
            >>> # Approve multiple tasks
            >>> tasks.bulk_complete_tasks(
            ...     task_ids=[12345, 12346, 12347],
            ...     action="Approve",
            ...     folder_key="5ebb73c3-..."
            ... )
        """
        payload = {
            "taskIds": task_ids,
            "actionName": action
        }

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        self.sdk.api_client.request(
            "POST",
            "/forms/TaskForms/BulkCompleteTasks",
            json=payload,
            headers=headers
        )

    def get_task_data(
        self,
        task_id: int,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get task form data by ID.

        Args:
            task_id: Task ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Task data dictionary

        Example:
            >>> tasks = TasksExt(sdk)
            >>> data = tasks.get_task_data(
            ...     task_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Form data: {data}")
        """
        params = {"taskId": task_id}

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/forms/TaskForms/GetTaskDataById",
            params=params,
            headers=headers
        )

        return response.json()

    def get_task_form(
        self,
        task_id: int,
        folder_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get task form layout/definition.

        Args:
            task_id: Task ID
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            Form layout dictionary

        Example:
            >>> tasks = TasksExt(sdk)
            >>> form = tasks.get_task_form(
            ...     task_id=12345,
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> print(f"Form fields: {form.get('fields')}")
        """
        params = {"taskId": task_id}

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/forms/TaskForms/GetTaskFormById",
            params=params,
            headers=headers
        )

        return response.json()

    def list_pending_tasks_for_user(
        self,
        folder_key: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List pending tasks for current user.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            top: Maximum number of results (optional)

        Returns:
            List of pending task dictionaries

        Example:
            >>> tasks = TasksExt(sdk)
            >>> my_tasks = tasks.list_pending_tasks_for_user(
            ...     folder_key="5ebb73c3-...",
            ...     top=20
            ... )
            >>> print(f"You have {len(my_tasks)} pending tasks")
        """
        return self.list_tasks(
            folder_key=folder_key,
            filter_query="Status eq 'Unassigned' or Status eq 'Pending'",
            order_by="CreationTime desc",
            top=top
        )

    def list_task_catalogs(
        self,
        folder_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List available task catalogs (task type definitions).

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)

        Returns:
            List of task catalog dictionaries

        Example:
            >>> tasks = TasksExt(sdk)
            >>> catalogs = tasks.list_task_catalogs(
            ...     folder_key="5ebb73c3-..."
            ... )
            >>> for catalog in catalogs:
            ...     print(f"{catalog['Name']}: {catalog['Description']}")
        """
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/TaskCatalogs",
            headers=headers
        )

        return response.json().get("value", [])
