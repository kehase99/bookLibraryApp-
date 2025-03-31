from datetime import datetime

def get_date_formats() -> list[dict]:
    """
    Returns a list of common date formats with examples, including German date format.
    """
    from datetime import datetime

    now = datetime(2025, 3, 22, 14, 30, 0)  # Example date and time

    formats = [
        {"format": "YYYY-MM-DD", "example": now.strftime("%Y-%m-%d")},
        {"format": "YYYY-MM-DDTHH:MM:SS", "example": now.strftime("%Y-%m-%dT%H:%M:%S")},
        {"format": "MM/DD/YYYY", "example": now.strftime("%m/%d/%Y")},
        {"format": "DD/MM/YYYY", "example": now.strftime("%d/%m/%Y")},
        {"format": "DD.MM.YYYY (German Format)", "example": now.strftime("%d.%m.%Y")},  # German format
        {"format": "Day, DD Month YYYY", "example": now.strftime("%A, %d %B %Y")},
        {"format": "DD-Mon-YYYY", "example": now.strftime("%d-%b-%Y")},
        {"format": "HH:MM:SS", "example": now.strftime("%H:%M:%S")},
        {"format": "HH:MM:SS AM/PM", "example": now.strftime("%I:%M:%S %p")},
        {"format": "Unix Timestamp", "example": int(now.timestamp())},
        {"format": "Month DD, YYYY", "example": now.strftime("%B %d, %Y")},
        {"format": "YYYYMMDD", "example": now.strftime("%Y%m%d")},
        {"format": "Day, DD Mon YYYY HH:MM:SS +Timezone", "example": now.strftime("%a, %d %b %Y %H:%M:%S +0000")},
        {"format": "YYYY-Www", "example": now.strftime("%Y-W%U")},
        {"format": "YYYY-DDD", "example": now.strftime("%Y-%j")},
    ]

    return formats


# Example usage
 

def date_type(value):
    try:
        return datetime.strftime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {value}. Expected format: YYYY-MM-DD")