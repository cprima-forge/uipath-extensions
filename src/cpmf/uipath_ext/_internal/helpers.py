"""Internal helper utilities for SDK extensions.

Provides shared functionality for header management, request handling,
and common operations across extension classes.
"""

from typing import Dict, Any, Optional
from uipath import UiPath


def get_folder_id_from_api(sdk: UiPath, folder_key: str) -> Optional[int]:
    """Get numeric folder ID from folder key via API.

    Args:
        sdk: UiPath SDK instance
        folder_key: Folder GUID key

    Returns:
        Numeric folder ID, or None if not found

    Raises:
        Exception: If API request fails
    """
    response = sdk.api_client.request(
        "GET",
        "/odata/Folders",
        headers={"x-uipath-folderkey": folder_key}
    )

    folders = response.json().get("value", [])

    for folder in folders:
        if folder.get("Key") == folder_key:
            return folder.get("Id")

    return None


def get_bucket_id_from_index(sdk: UiPath, index_name: str, folder_key: str) -> Optional[int]:
    """Get bucket ID from Context Grounding index.

    Args:
        sdk: UiPath SDK instance
        index_name: Name of the Context Grounding index
        folder_key: Folder GUID key

    Returns:
        Numeric bucket ID, or None if not found

    Raises:
        Exception: If API request fails or index not found
    """
    # Get the index to find bucket name
    index = sdk.context_grounding.retrieve(
        name=index_name,
        folder_key=folder_key
    )

    bucket_name = index.data_source.bucketName

    # Get folder ID for bucket lookup
    folder_id = get_folder_id_from_api(sdk, folder_key)
    if not folder_id:
        raise ValueError(f"Folder not found: {folder_key}")

    # Get bucket ID
    buckets_response = sdk.api_client.request(
        "GET",
        "/odata/Buckets",
        headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}
    )

    buckets = buckets_response.json().get("value", [])

    for bucket in buckets:
        if bucket.get("Name") == bucket_name:
            return bucket.get("Id")

    return None


def make_bucket_request(
    sdk: UiPath,
    method: str,
    endpoint: str,
    folder_id: int,
    **kwargs: Any
) -> Any:
    """Make a request to a bucket endpoint with proper headers.

    Automatically adds X-UIPATH-OrganizationUnitId header for bucket operations.

    Args:
        sdk: UiPath SDK instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        folder_id: Numeric folder/organization unit ID
        **kwargs: Additional arguments passed to api_client.request

    Returns:
        HTTP response

    Raises:
        Exception: If request fails
    """
    headers = kwargs.get("headers", {})
    headers["X-UIPATH-OrganizationUnitId"] = str(folder_id)
    kwargs["headers"] = headers

    return sdk.api_client.request(method, endpoint, **kwargs)
