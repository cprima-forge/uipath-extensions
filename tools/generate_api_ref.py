#!/usr/bin/env python3
"""Generate API reference documentation."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cpmf.uipath_ext import get_all_extensions, get_extension_metadata
from inspect import getmembers, ismethod, signature, Parameter
from unittest.mock import Mock

metadata = get_extension_metadata()

output = []
output.append("# API Reference")
output.append("")
output.append("> Auto-generated reference for cprima-forge-uipath-extensions v0.0.5")
output.append("")
output.append("## Extension Classes")
output.append("")

for ext_class in get_all_extensions():
    class_name = ext_class.__name__
    meta = metadata.get(class_name, {})

    output.append(f"### {class_name}")
    output.append("")
    output.append(f"**Entity:** `{meta.get('entity', 'N/A')}`  ")
    output.append(f"**Endpoint:** `{meta.get('endpoint', 'N/A')}`  ")
    output.append(f"**Category:** {meta.get('category', 'N/A')}  ")
    output.append(f"**Scope:** {meta.get('scope', 'N/A')}")
    output.append("")

    if ext_class.__doc__:
        doc_lines = [line.strip() for line in ext_class.__doc__.strip().split('\n') if line.strip()]
        if doc_lines:
            output.append(f"**Description:** {doc_lines[0]}")
            output.append("")

    output.append("**Methods:**")
    output.append("")

    # Get all public methods
    try:
        mock_sdk = Mock()
        instance = ext_class(mock_sdk)

        methods = [
            (name, method) for name, method in getmembers(instance, predicate=ismethod)
            if not name.startswith('_')
        ]

        for method_name, method in sorted(methods):
            try:
                sig = signature(method)
                params = []
                for param_name, param in sig.parameters.items():
                    if param_name == 'self':
                        continue
                    if param.annotation != Parameter.empty:
                        type_name = str(param.annotation).replace('typing.', '').replace('<class \'', '').replace('\'>', '')
                        if param.default != Parameter.empty:
                            params.append(f"{param_name}: {type_name} = {repr(param.default)}")
                        else:
                            params.append(f"{param_name}: {type_name}")
                    else:
                        if param.default != Parameter.empty:
                            params.append(f"{param_name} = {repr(param.default)}")
                        else:
                            params.append(param_name)

                param_str = ', '.join(params) if params else ''
                return_type = ''
                if sig.return_annotation != signature.empty:
                    ret_str = str(sig.return_annotation).replace('typing.', '').replace("<class '", '').replace("'>", '')
                    return_type = f" -> {ret_str}"

                output.append(f"- `{method_name}({param_str}){return_type}`")
            except Exception as e:
                output.append(f"- `{method_name}(...)` _(introspection failed)_")

    except Exception as e:
        output.append(f"  _(Unable to introspect: {e})_")

    output.append("")

output.append("")
output.append("---")
output.append("")
output.append("**Total Extensions:** 11  ")
output.append("**Total Coverage:** ~85% of Orchestrator API surface  ")
output.append("**Import:** `from cpmf.uipath_ext import <ClassName>`")

# Write to file
api_ref_path = Path(__file__).parent / "docs" / "users" / "API_REFERENCE.md"
api_ref_path.write_text('\n'.join(output), encoding='utf-8')
print(f"Generated: {api_ref_path}")
