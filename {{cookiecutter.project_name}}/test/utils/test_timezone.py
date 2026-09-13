from datetime import timedelta
from zoneinfo import ZoneInfo

from {{cookiecutter.package_name}}.utils import timezone as tz_utils


def test_now_returns_aware_utc_datetime_when_use_tz():
    current = tz_utils.now()
    assert current.tzinfo is not None
    assert current.utcoffset() == timedelta(0)


def test_now_returns_naive_datetime_when_use_tz_disabled(monkeypatch):
    monkeypatch.setattr(tz_utils.settings, "USE_TZ", False)
    current = tz_utils.now()
    assert current.tzinfo is None


def test_get_fixed_timezone_from_timedelta():
    fixed = tz_utils.get_fixed_timezone(timedelta(hours=5, minutes=30))
    assert fixed.utcoffset(None) == timedelta(hours=5, minutes=30)
    assert fixed.tzname(None) == "+0530"


def test_get_fixed_timezone_from_int_minutes():
    fixed = tz_utils.get_fixed_timezone(-330)
    assert fixed.utcoffset(None) == timedelta(minutes=-330)
    assert fixed.tzname(None) == "-0530"


def test_get_default_timezone_uses_settings():
    assert tz_utils.get_default_timezone() == ZoneInfo("UTC")
    assert isinstance(tz_utils.get_default_timezone(), ZoneInfo)
