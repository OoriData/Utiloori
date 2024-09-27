# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.json
'''
Tools for JSON
'''
from typing import List


def find_long_strings(data, threshold: int, path: List[str] | None = None) -> List[str]:
    '''
    Recursive search for long strings in a JSON-like object (lists/dicts with strings, numbers, bools…)

    Args:
        data - top level object for the search
        threshold - how long is considered a long string
        path (defaults to empty) - recursive accumulator generally not passed in from original caller
    '''
    if path is None: path = []  # noqa E701
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [f"['{key}']"]
            results.extend(find_long_strings(value, threshold, path=new_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = path + [f"[{i}]"]
            results.extend(find_long_strings(item, threshold, path=new_path))
    elif isinstance(data, str) and len(data) > threshold:
        results.append(''.join(path))
    return results
