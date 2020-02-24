from datetime import datetime


# Generate the datetime for the current day at a given hour and given minute
def get_time_at(hour: int, minute: int) -> datetime:
    now = datetime.now()
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


