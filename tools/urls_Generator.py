from datetime import date, timedelta


def dates_in_year(year: int) -> list[str]:
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    fmt = "%Y%m%d"

    days = []
    current = start
    while current < end:
        days.append(current.strftime(fmt))
        current += timedelta(days=1)

    return days


def generate_urls_by_years(startYear: int, endYear: int) -> list[str]:
    urls = []
    
    for year in range(startYear, endYear+1):
        dates = dates_in_year(year=year)
        for date in dates:
            url = f"https://www.info.gov.hk/gia/general/{date[:6]}/{date[6:]}.htm"
            urls.append(url)
    
    return urls




# # Example
# print(dates_in_year(2025))
