"""
cpmf.uipath_ext - Community-built extensions for the UiPath Python SDK

This package provides utilities, helpers, and integration patterns
for working with the UiPath Python SDK.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cprima-forge-uipath-extensions")
except PackageNotFoundError:
    # Package is not installed, use development version
    __version__ = "0.0.0.dev"

__all__ = ["__version__"]
