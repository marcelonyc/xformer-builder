from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def json_object_converter(data: dict[str, Any]) -> dict[str, Any]:
    """JSON serializer for objects not serializable by default json code"""
    datetime_fields = {
        k: convert_datetime_to_gmt(data[k])
        for k in data.keys()
        if isinstance(data[k], datetime)
    }

    return {**data, **datetime_fields}
