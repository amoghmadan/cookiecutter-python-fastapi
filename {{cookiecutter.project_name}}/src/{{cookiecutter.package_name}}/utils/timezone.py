from datetime import UTC, datetime, timedelta, timezone
from functools import lru_cache
from zoneinfo import ZoneInfo

from {{cookiecutter.package_name}}.conf import settings


def now() -> datetime:
    """
    Timezone based datetime.now.
    return: datetime
    """
    return datetime.now(tz=UTC if settings.USE_TZ else None)


def get_fixed_timezone(offset) -> timezone:
    """Return a tzinfo instance with a fixed offset from UTC."""
    if isinstance(offset, timedelta):
        offset = int(offset.total_seconds() // 60)
    sign = "-" if offset < 0 else "+"
    h, m = divmod(abs(offset), 60)
    hhmm = f"{h:02d}{m:02d}"
    name = sign + hhmm
    return timezone(timedelta(minutes=offset), name)


@lru_cache
def get_default_timezone() -> ZoneInfo:
    """
    Return the default time zone as a tzinfo instance.

    This is the time zone defined by settings.TIME_ZONE.
    """
    return ZoneInfo(settings.TIME_ZONE)


__all__ = ["get_default_timezone", "get_fixed_timezone", "now", "timedelta"]
