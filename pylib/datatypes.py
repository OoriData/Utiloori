# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.datatypes

from uuid import UUID

def validate_uuid(uuid_str):
    ''' Validate UUID string '''
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False

