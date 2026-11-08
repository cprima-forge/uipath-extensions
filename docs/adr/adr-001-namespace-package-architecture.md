# ADR-001: Namespace Package Architecture

**Status:** Accepted

**Date:** 2025-10-27

**Decision Makers:** Christian Prior-Mamulyan

**Technical Story:** Establishing the package import structure for the cprima-forge UiPath extensions ecosystem

---

## Context

The cprima-forge initiative aims to create multiple Python packages that extend and enhance the UiPath Python SDK. We need to decide on the package naming and import structure for these extensions.

### Requirements

1. Multiple related packages should be able to coexist under a common organizational namespace
2. Each sub-package should be independently installable and distributable
3. The import structure should be intuitive and prevent naming conflicts
4. The solution should follow Python packaging best practices
5. Users should be able to install only the components they need

### Problem

Without a namespace package strategy, we would face these issues:

- **Naming conflicts**: Multiple packages like `uipath-extensions-orchestrator`, `uipath-extensions-dataservice` would create long, awkward names
- **Import inconsistency**: Each package would have its own top-level import (e.g., `import uipath_orchestrator`, `import uipath_dataservice`)
- **Namespace pollution**: Installing multiple packages would pollute the global namespace with multiple unrelated top-level imports
- **Organization**: No clear indication that packages belong to the same ecosystem

## Decision

We will use **PEP 420 implicit namespace packages** with **pkgutil path extension** to create a `cpmf` (cprima-forge) namespace.

### Implementation Details

**Package structure:**
```
cpmf/                           # Namespace root (no __init__.py in final deployment)
├── __init__.py                 # Contains: __path__ = __import__("pkgutil").extend_path(__path__, __name__)
└── uipath_ext/                 # This package
    └── __init__.py
```

**Import pattern:**
```python
from cpmf.uipath_ext import some_utility
```

**PyPI package name:** `cprima-forge-uipath-extensions`

**Namespace declaration in `src/cpmf/__init__.py`:**
```python
"""
cpmf - cprima-forge namespace package

This is a namespace package that allows multiple cprima-forge projects
to coexist under the 'cpmf' namespace.
"""

__path__ = __import__("pkgutil").extend_path(__path__, __name__)
```

### Why pkgutil.extend_path()?

We chose pkgutil path extension over pure PEP 420 implicit namespaces for better compatibility:

1. **Explicit documentation**: The `__init__.py` with docstring clearly indicates this is a namespace package
2. **Path extension**: Allows portions of the namespace to be installed in different locations
3. **Backward compatibility**: Works with older tooling that expects `__init__.py` files
4. **Future flexibility**: Easy to add namespace-level utilities or configuration if needed

## Rationale

### Benefits

1. **Unified namespace**: All cprima-forge packages live under `cpmf.*`
2. **Clear organization**: `cpmf.uipath_ext`, `cpmf.langchain_ext`, etc. clearly indicate related projects
3. **Independent distribution**: Each sub-package can be released independently on PyPI
4. **Selective installation**: Users install only what they need: `pip install cprima-forge-uipath-extensions`
5. **Namespace protection**: `cpmf` is a distinctive prefix unlikely to conflict with other packages
6. **Professional appearance**: Consistent with established Python projects (e.g., `azure.*`, `google.*`)

### Trade-offs

1. **Slightly longer imports**: `from cpmf.uipath_ext` vs. just `from uipath_ext`
2. **Namespace coordination**: Must ensure different cprima-forge packages don't conflict within the namespace
3. **Documentation complexity**: Need to explain namespace package concept to contributors
4. **Package discovery**: Users need to understand the relationship between PyPI name (`cprima-forge-uipath-extensions`) and import name (`cpmf.uipath_ext`)

## Alternatives Considered

### Alternative 1: Flat Package Structure
```python
import uipath_extensions
```

**Rejected because:**
- Doesn't scale to multiple related packages
- Generic name likely to conflict with other projects
- No clear organizational identity

### Alternative 2: Prefix-based Flat Packages
```python
import cpmf_uipath_ext
```

**Rejected because:**
- Ugly underscore-heavy import names
- Doesn't provide true namespace isolation
- Loses the organizational hierarchy

### Alternative 3: Single Monolithic Package
```python
from cpmf import uipath, langchain, other_tools
```

**Rejected because:**
- Forces users to install everything together
- Harder to maintain and version independently
- Larger dependency footprint

### Alternative 4: Pure PEP 420 (No `__init__.py`)
```python
# No __init__.py in cpmf/
```

**Rejected because:**
- Less explicit about namespace intent
- Some older tools may not handle correctly
- Harder to document the namespace package nature

## Consequences

### Positive

- Clean, professional import structure
- Scalable for future cprima-forge packages
- Each package can evolve independently
- Clear organizational branding
- Follows Python packaging best practices

### Negative

- Slightly more complex for first-time contributors to understand
- Need to document the namespace package approach
- PyPI package name differs from import name (common but can be confusing)

### Neutral

- Requires coordination when adding new packages to the `cpmf` namespace
- Need to maintain consistency across all cprima-forge Python packages

## Compliance

This decision complies with:

- **PEP 420** - Implicit Namespace Packages
- **PEP 517** - Build system independence
- **PEP 621** - Project metadata in pyproject.toml

## References

- [PEP 420 - Implicit Namespace Packages](https://peps.python.org/pep-0420/)
- [Python Packaging User Guide - Namespace Packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/)
- [setuptools - Namespace Packages](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#namespace-packages)

## Implementation

- **Repository:** github.com/cprima-forge/uipath-extensions
- **Implemented in:** Initial commit (6f41fe5)
- **Files:**
  - `src/cpmf/__init__.py` - Namespace declaration
  - `src/cpmf/uipath_ext/__init__.py` - Package implementation
  - `pyproject.toml` - Package configuration

## Notes

Future cprima-forge packages should follow this pattern:
- Create under `cpmf.*` namespace
- Use `pkgutil.extend_path()` in namespace `__init__.py`
- Choose descriptive sub-package names
- Document the namespace package architecture
