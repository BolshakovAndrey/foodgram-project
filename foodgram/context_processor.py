import datetime as dt
from django import template


def year(request):
    """
    Adds a variable with the current year.
    """
    now = dt.datetime.now()

    return {"year": now.year}
