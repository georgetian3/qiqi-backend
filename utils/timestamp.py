from datetime import datetime
import pytz

def to_utc(timestamp: datetime) -> datetime:
    return timestamp.astimezone(pytz.UTC)