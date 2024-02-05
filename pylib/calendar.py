# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.calendar

from datetime import time, datetime, timezone, timedelta


def time_plus_delta(t: time, tdelt: timedelta) -> time:
    '''
    Add a timedelta to a time object. Python forbids you from doing this naively, with a time & timedelta object,
    because of the ambiguity when crossing the midnight border.
    
    This function does that, but with an explicit check to forbid such a crossing
    '''
    if isinstance(t, datetime):
        import warnings
        warnings.warn(
            'time_plus_delta: t is a datetime, not a time object. Just use simple arithmetic instead of this function.')
    start = datetime(2000, 1, 1, hour=t.hour, minute=t.minute, second=t.second, tzinfo=timezone.utc)
    end = start + tdelt
    if end.day != start.day:
        msg = 'Adding time delta crosses midnight boundary'
        raise ValueError(msg)
    return end.time()
