"""
Handle database querying.

By abstracting it here we can just use dicts for testing.
"""

from pathlib import Path

import jsonpickle

from ..objects import datastructures  # needed for unpickling.

martyrology = []


def eval_year(year, yearless):
    """

    Parameters
    ----------
    year :

    yearless :

    as_list :
         (Default value = True)

    Returns
    -------

    """
    yeared = {}
    for row in yearless:
        if not row:
            continue
        try:
            date = row.date.resolve(year)
        except AttributeError:
            print(row)
        try:
            yeared[date].append(row)
        except KeyError:
            yeared[date] = [row]

    return yeared


def load_martyrology():
    """"""
    global martyrology
    with Path("backend/api/martyrology.json").open() as f:
        raw_tables["martyrology"] = jsonpickle.decode(
            f.read(), classes=[datastructures.Date, datastructures.Martyrology]
        )


years = {}

year_tables = {"martyrology": None}
raw_tables = {}


def raw_query(day, table):
    """
    Query table for data on day.

    Parameters
    ----------
    day :

    table :


    Returns
    -------
    """
    global raw_tables, year_tables
    year = day.year
    try:
        return year_tables[table][year][day].render(year)
    except (KeyError, TypeError):
        this_year = eval_year(year, raw_tables[table], False)
        try:
            year_tables[table][year] = this_year
        except (KeyError, TypeError):
            year_tables[table] = {year: this_year}
        return year_tables[table][year][day].render(year)


def init():
    """Start database."""
    load_martyrology()
