'''
pytest test

or

pytest test/test_calendar.py
'''
import utiloori.calendar

def test_time_plus_delta():
    from datetime import time, timedelta
    t = time(12, 0, 0)
    tdelt = timedelta(hours=1)
    assert utiloori.calendar.time_plus_delta(t, tdelt) == time(13, 0, 0)
    t = time(23, 0, 0)
    tdelt = timedelta(hours=1)
    assert utiloori.calendar.time_plus_delta(t, tdelt) == time(0, 0, 0)
