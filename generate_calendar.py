import csv


def load_qualenia():
    headers = [
        "qualenia",
        "month_id",
        "month_name",
        "constellation",
        "season",
    ]
    qualenia = []

    with open("./raw/qualenia.csv") as f:
        # skip header row
        next(f)
        reader = csv.DictReader(f, headers)
        qualenia = [_ for _ in reader]

    return qualenia


def qualenia_dates():
    qualenia = load_qualenia()

    dates = []
    for month in qualenia:
        for day in range(32):
            _day = day + 1
            dates.append({**month, **{"day": _day}})
    return dates


def qualenia_years():
    starting_year = 714
    qualenia = qualenia_dates()

    years = []
    for day in qualenia:
        _day = day["day"]
        _day = f"0{_day}" if _day < 10 else _day
        _month = day["month_id"]
        for year in range(starting_year, starting_year + 101):
            years.append({**day, **{"year": year, "date": f"{year}-{_month}-{_day}"}})

    return years

def main():
    data = qualenia_years()
    data.sort(key=lambda v: v["date"])
    headers = [
        "date",
        "year",
        "month_id",
        "day",
        "qualenia",
        "month_name",
        "constellation",
        "season",
    ]
    with open("./exports/export.csv", "w", newline="") as f:
        _writer = csv.DictWriter(f, headers)
        _writer.writeheader()
        _writer.writerows(data)


if __name__ == "__main__":
    main()
