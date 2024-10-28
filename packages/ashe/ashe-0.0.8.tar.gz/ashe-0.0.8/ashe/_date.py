import calendar
from datetime import datetime, timedelta

from typing import List, Union


def today(date_type: str = "str") -> Union[str, datetime.date]:
    _today = datetime.today().date()
    if date_type == "str":
        _today = str(_today)
    return _today


def yesterday(date_type: str = "str") -> Union[str, datetime.date]:
    _yesterday = today(date_type="date") + timedelta(days=-1)
    if date_type == "str":
        _yesterday = str(_yesterday)
    return _yesterday


def tomorrow(date_type: str = "str") -> Union[str, datetime.date]:
    _tomorrow = today(date_type="date") + timedelta(days=1)
    if date_type == "str":
        _tomorrow = str(_tomorrow)
    return _tomorrow


def week() -> int:
    return today(date_type="date").isocalendar()[1]


def month() -> int:
    return today(date_type="date").month


def year() -> int:
    return today(date_type="date").year


def get_interval_days(start: str = None, end: str = None, interval: int = None, reverse: bool = False,
                      date_type: str = "str") -> List[Union[str, datetime.date]]:
    if start is not None and end is not None and interval is not None:
        raise ValueError("three parameters (start end interval) cannot be present at the same time!")
    elif start is not None and end is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        interval = (end_date - start_date).days + 1
    elif start is not None and interval is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
    elif end is not None and interval is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        start_date = end_date - timedelta(days=interval - 1)
    elif start is None and end is None and interval is not None:
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=interval - 1)
    else:
        raise ValueError("please check parameter, single parameter only support interval!")

    day_list = []
    for day_delta in range(interval):
        _day = start_date + timedelta(days=day_delta)
        if date_type == "str":
            day_list.append(str(_day))
        else:
            day_list.append(_day)

    if reverse:
        day_list.reverse()

    return day_list


def get_week_days(offset: int = 0, date_type: str = "str") -> List[Union[str, datetime.date]]:
    _today = today(date_type="date")
    week_day = _today.weekday()
    _week_start_date = _today + timedelta(days=-week_day, weeks=offset)
    _week_end_date = _today + timedelta(days=-(week_day-6), weeks=offset)
    return get_interval_days(start=str(_week_start_date), end=str(_week_end_date), date_type=date_type)


def get_month_days(offset: int = 0, date_type: str = "str") -> List[Union[str, datetime.date]]:
    total_month = month() + offset
    _year = year() + (total_month-1)//12
    _month = 12 if total_month % 12 == 0 else total_month % 12

    month_days = calendar.monthrange(_year, _month)[1]
    _month_start_date = datetime(year=_year, month=_month, day=1).date()
    _month_end_date = datetime(year=_year, month=_month, day=month_days).date()
    return get_interval_days(start=str(_month_start_date), end=str(_month_end_date), date_type=date_type)
