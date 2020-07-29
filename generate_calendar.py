import csv
import sqlite3
from pathlib import Path
import os


def load_qualenia():
    headers = [
        "qualenia",
        "month",
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
    day_of_qualenia = 0
    day_of_year = 0
    current_qualenia = 1
    
    for month in qualenia:
        if month["qualenia"] != current_qualenia:
            current_qualenia = month["qualenia"]
            day_of_year = 0
        
        for day in range(32):
            day_of_qualenia += 1
            day_of_year += 1
            _day = day + 1
            dates.append(
                {
                    **month,
                    **{
                        "day": _day,
                        "day_of_qualenia": day_of_qualenia,
                        "day_of_year": day_of_year,
                    },
                }
            )
    return dates


def qualenia_years():
    qualenia = qualenia_dates()

    years = []
    year = 714
    current_qualenia = '1'

    # 25 iterations of qualenia 4 yr cycle
    for _ in range(25):

        # for every day in a qualenia cycle
        for day in qualenia:
            if day["qualenia"] != current_qualenia:
                current_qualenia = day["qualenia"]
                year += 1
            _day = day["day"]
            _day = f"0{_day}" if _day < 10 else _day
            _month = day["month"]
            _qualenia = day["qualenia"]
            
            # for year in range(starting_year, starting_year + 101):
            _date_id = f"{year}{_qualenia}{_month}{_day}"
            _date = f"{year}-{_qualenia}-{_month}-{_day}"
            years.append({**day, **{"year": year, "date": _date, "date_id": _date_id}})
    return years

def make_calendar_csv():
    data = qualenia_years()
    data.sort(key=lambda v: v["date_id"])
    headers = [
        "date_id",
        "day_of_qualenia",
        "day_of_year",
        "year",
        "qualenia",
        "month",
        "day",
        "date",
        "month_name",
        "constellation",
        "season",
    ]
    with open("./exports/export.csv", "w", newline="") as f:
        _writer = csv.DictWriter(f, headers)
        _writer.writeheader()
        _writer.writerows(data)

def setup_db():
    db_path = Path("db.sqlite")
    if db_path.exists:
        os.remove(db_path)

    db = sqlite3.connect("db.sqlite")
    qry_create_table = """
    create table calendar (
        date_id int,
        day_of_qualenia int,
        day_of_year int,
        year int,
        qualenia int,
        month int,
        day int,
        date varchar(10),
        month_name varchar(50),
        constellation varchar(50),
        season varchar(50)
    );
    """
    db.execute(qry_create_table)
    db.commit()
    
    return db

def make_calendar_db():
    data = qualenia_years()
    data.sort(key=lambda v: v["date_id"])
    headers = [
        "date_id",
        "day_of_qualenia",
        "day_of_year",
        "year",
        "qualenia",
        "month",
        "day",
        "date",
        "month_name",
        "constellation",
        "season",
    ]

    # flatten data
    values = []
    for rcd in data:
        _row = []
        for hdr in headers:
            _row.append(rcd[hdr])
        values.append(tuple(_row))

    # prepare db
    db = setup_db()
    qry_insert = "insert into calendar ('{headers}') values ({placeholders})".format(
        headers="','".join(headers),
        placeholders=",".join(["?" for _ in range(len(headers))])
    )

    # insert data
    db.executemany(qry_insert, values)
    db.commit()
    

def main():
    make_calendar_csv()
    make_calendar_db()


if __name__ == "__main__":
    main()
