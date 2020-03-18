from datetime import datetime


def get_time_at(hour: int, minute: int) -> datetime:
    """
    Helper which generate the datetime for the current day at a given hour and given minute
    """
    now = datetime.now()
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
