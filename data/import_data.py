#!/usr/bin/env python3

import csv

import click

from utils import mongo_connection as conn

headers_translations = {
    "regiao": "region",
    "estado": "state",
    "data": "date",
    "casosNovos": "new_cases",
    "casosAcumulados": "acumulated_cases",
    "obitosNovos": "new_deaths",
    "obitosAcumulados": "acumulated_deaths",
}


def head(list_):
    return list_[0]


def tail(list_):
    return list_[1:]


def _get_headers(row):
    headers = [header for header in row[0].split(";")]
    translated_headers = [headers_translations[header] for header in headers]

    return translated_headers


def _get_body(rows):
    return [r[0].split(";") for r in rows]


def _format_data_dict(headers, body):
    return [
        {
            headers[0]: bd[0],
            headers[1]: bd[1],
            headers[2]: bd[2],
            headers[3]: bd[3],
            headers[4]: bd[4],
            headers[5]: bd[5],
            headers[6]: bd[6],
        }
        for bd in body
    ]


@click.command()
@click.argument("input", type=click.File("r"))
@click.option("-d", "--date", required=False, default=0)
def main(input, date):
    if date is 0:
        date = input.name[8:-4]

    csv_reader = csv.reader(input, delimiter=",")
    rows = [row for row in csv_reader]
    if not click.confirm(f"Will import {len(rows)} rows for date {date}, proceed?"):
        print("Process aborted")
        return

    headers = _get_headers(head(rows))
    body = _get_body(tail(rows))

    formated_data = _format_data_dict(headers, body)
    print("Formatted data")

    db = conn.get_connection()
    collection_name = f"situation_{date}"
    final_result = db[collection_name].insert_many(formated_data)
    print(f"Finished inserting data into {collection_name}")


if __name__ == "__main__":
    main()
