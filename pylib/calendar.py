# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.calendar


def time_plus_delta(t, tdelt):
    '''
    Add a timedelta to a time object. Python forbids you from doing this naively, with a time & timedelta object,
    because of the ambiguity when crossing the midnight border.
    
    This function does that, but with an explicit check to forbid such a crossing
    '''
    from datetime import datetime, timezone
    start = datetime(2000, 1, 1, hour=t.hour, minute=t.minute, second=t.second, tzinfo=timezone.utc)
    end = start + tdelt
    if end.day != start.day:
        msg = 'Adding time delta crosses midnight boundary'
        raise ValueError(msg)
    return end.time()
