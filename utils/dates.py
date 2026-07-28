
from datetime import date, datetime

from utils.constants import DATE_FORMAT


def parse_date(date_string: str) -> date | None:
    """
    Parse a date string into a date object.
    Return None if parsing fails.
    """
    try:
        return datetime.strptime(date_string, DATE_FORMAT).date()
    except ValueError:
        return None