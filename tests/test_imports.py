"""Smoke tests to verify all modules import correctly."""


def test_import_version():
    """Verify __version__ is accessible."""
    from cpmf.uipath_ext import __version__
    assert __version__
    assert isinstance(__version__, str)


def test_import_all_extensions():
    """Verify all 11 extension classes can be imported."""
    from cpmf.uipath_ext import (
        AssetsExt,
        BucketExtensions,
        ContextGroundingExt,
        FolderManagementExt,
        FolderUtils,
        JobsExt,
        LibrariesExt,
        ProcessesExt,
        QueuesExt,
        SchedulesExt,
        TasksExt,
    )
    # All imports succeeded if we get here
    assert AssetsExt is not None
    assert JobsExt is not None
    assert QueuesExt is not None
    assert ProcessesExt is not None
    assert SchedulesExt is not None
    assert LibrariesExt is not None
    assert TasksExt is not None
    assert FolderUtils is not None
    assert FolderManagementExt is not None
    assert BucketExtensions is not None
    assert ContextGroundingExt is not None


def test_get_all_extensions():
    """Verify get_all_extensions returns all 11 classes."""
    from cpmf.uipath_ext import get_all_extensions
    extensions = get_all_extensions()
    assert len(extensions) == 11


def test_get_extension_metadata():
    """Verify extension metadata is complete."""
    from cpmf.uipath_ext import get_extension_metadata
    metadata = get_extension_metadata()
    assert len(metadata) == 11
    assert "AssetsExt" in metadata
    assert metadata["AssetsExt"]["endpoint"] == "/odata/Assets"


def test_telemetry_functions():
    """Verify telemetry control functions exist."""
    from cpmf.uipath_ext import disable_telemetry, is_telemetry_enabled
    assert callable(disable_telemetry)
    assert callable(is_telemetry_enabled)
