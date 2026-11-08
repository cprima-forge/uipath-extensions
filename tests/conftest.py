"""Pytest fixtures for cpmf-uipath-extensions tests."""
import sys
from unittest.mock import MagicMock, Mock

import pytest


# Mock the uipath module before any imports
class MockUiPath:
    """Mock UiPath SDK class for testing."""

    def __init__(self, *args, **kwargs):
        self.api_client = Mock()
        self.api_client.request = MagicMock()


# Create mock uipath module
mock_uipath = MagicMock()
mock_uipath.UiPath = MockUiPath
sys.modules["uipath"] = mock_uipath


@pytest.fixture
def mock_sdk():
    """Create a mock UiPath SDK instance."""
    sdk = Mock()
    sdk.api_client = Mock()
    sdk.api_client.request = MagicMock()
    return sdk


@pytest.fixture
def mock_response():
    """Factory for mock API responses."""
    def _make_response(data):
        response = Mock()
        response.json.return_value = data
        return response
    return _make_response
