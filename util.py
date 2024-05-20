from datetime import datetime


def get_current_time():
    return datetime.now().strftime("%B %d, %Y %I:%M %p")
