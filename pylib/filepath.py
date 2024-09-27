# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.filepath
import inspect

from pathlib import Path


def obj_file_path_parent(obj):
    '''Cross-platform Python trick to get the path to a file containing a given object'''
    # Should already be an absolute path
    # from os.path import abspath
    # return abspath(inspect.getsourcefile(obj))
    return Path(inspect.getsourcefile(obj)).parent
