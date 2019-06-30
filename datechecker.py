import datetime


def month_check(month):
    if month > 0 and month <= 12:  # If month is between 1 and 12, return True.
        return True
    else:
        return False


def day_check(month, day):
    days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if 0 < day <= days_in_month[month]:
        return True
    else:
        return False


def year_check(year):
    # Check if year has between 1 to 4 numbers and return True.
    if len(year) >= 1 and len(year) <= 4:
        return True
    else:
        return False


def valid_date(day, month, year):
    today = datetime.date.today()
    if year < today.year:
        return False
    elif year == today.year:
        if month < today.month:
            return False
        elif month == today.month:
            if day < today.day:
                return False
            else:
                return True
        else:
            return True
    else:
        return True
