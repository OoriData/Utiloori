'''
pytest test

or

pytest test/test_calendar.py
'''
from datetime import time, timedelta

import pytest

import utiloori.calendar

def test_time_plus_delta():
    t = time(12, 0, 0)
    tdelt = timedelta(hours=1)
    assert utiloori.calendar.time_plus_delta(t, tdelt) == time(13, 0, 0)
    t = time(22, 59, 59)
    tdelt = timedelta(hours=1)
    assert utiloori.calendar.time_plus_delta(t, tdelt) == time(23, 59, 59)


def test_time_plus_delta_overrun():
    with pytest.raises(ValueError):
        t = time(23, 0, 0)
        tdelt = timedelta(hours=1)
        utiloori.calendar.time_plus_delta(t, tdelt)
