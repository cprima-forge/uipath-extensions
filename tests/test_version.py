"""Tests for version and telemetry functionality."""
import os


def test_version_format():
    """Verify version follows semver pattern or dev version."""
    from cpmf.uipath_ext import __version__
    # Should be X.Y.Z, X.Y.Z.dev, or 0.0.0.dev
    assert __version__
    assert isinstance(__version__, str)
    # Either dev version or semver
    if "dev" in __version__:
        assert __version__ == "0.0.0.dev"
    else:
        parts = __version__.split(".")
        assert len(parts) >= 3
        for part in parts[:3]:
            assert part.isdigit()


def test_telemetry_disable():
    """Test telemetry can be disabled."""
    from cpmf.uipath_ext import disable_telemetry, is_telemetry_enabled

    # Clear any existing setting
    os.environ.pop("UIPATH_TELEMETRY_ENABLED", None)

    # Initially enabled (default)
    assert is_telemetry_enabled()

    # Disable it
    disable_telemetry()
    assert not is_telemetry_enabled()

    # Clean up
    os.environ.pop("UIPATH_TELEMETRY_ENABLED", None)


def test_telemetry_env_var():
    """Test telemetry respects environment variable."""
    from cpmf.uipath_ext import is_telemetry_enabled

    # Clear any existing setting
    os.environ.pop("UIPATH_TELEMETRY_ENABLED", None)

    # Set to false
    os.environ["UIPATH_TELEMETRY_ENABLED"] = "false"
    assert not is_telemetry_enabled()

    # Set to true
    os.environ["UIPATH_TELEMETRY_ENABLED"] = "true"
    assert is_telemetry_enabled()

    # Clean up
    os.environ.pop("UIPATH_TELEMETRY_ENABLED", None)
