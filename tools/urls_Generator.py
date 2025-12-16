import datetime
import calendar

def generate_dates(year: int, month: int) -> list[str]:
    """
    Generate a list of all dates for a specific year and month.

    :param year: e.g., 2025
    :param month: 1–12
    :return: list of datetime.date objects
    """
    fmt = "%Y%m%d"
    _, num_days = calendar.monthrange(year, month)

    return [
        datetime.date(year, month, day).strftime(fmt)
        for day in range(1, num_days + 1)
    ]


def generate_urls_by_years(year: int, month: int) -> list[str]:
    urls = []
    
    dates = generate_dates(year=year, month=month)
    for date in dates:
        url = f"https://www.info.gov.hk/gia/general/{date[:6]}/{date[6:]}.htm"
        urls.append(url)
    
    return urls

def generate_url_by_date(date: str) -> str:

    return f"https://www.info.gov.hk/gia/general/{date[:6]}/{date[6:]}.htm"



# # Example
# print(dates_in_year(2025))
