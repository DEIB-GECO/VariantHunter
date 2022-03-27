"""
    Utilities
"""

from datetime import datetime, timedelta

start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
""" 
Reference date for database dates 
"""


def compute_weeks_from_date(date):
    """
    Compute weeks values starting from the date string of the last day of the 4th week
    Args:
        date: String representing the date of the last day of the 4th week

    Returns: A dictionary identifying all the 4 weeks

    """
    w = {}
    w['w4_end'] = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    w['w4_begin'] = w['w4_end'] - 7
    w['w3_end'] = w['w4_begin'] - 1
    w['w3_begin'] = w['w3_end'] - 7
    w['w2_end'] = w['w3_begin'] - 1
    w['w2_begin'] = w['w2_end'] - 7
    w['w1_end'] = w['w2_begin'] - 1
    w['w1_begin'] = w['w1_end'] - 7
    return w


def compute_diff_from_date(date):
    """
    Compute diff from the start_date from date
    Args:
        date: String representing the date to be considered

    Returns: Difference from the start date

    """
    diff = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    return diff


def compute_date_from_diff(diff):
    """
    Compute date value from diff from the start_date
    Args:
        diff: Difference from the start date

    Returns: A string representing the date

    """
    date= start_date + timedelta(days=diff)
    return date.strftime("%Y-%m-%d")
