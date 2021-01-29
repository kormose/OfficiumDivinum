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
    p = Path("./backend/api/martyrology.json").resolve()
    if not p.exists():
        p = Path("~/OfficiumDivinum/backend/api/martyrology.json").expanduser()
    with p.open() as f:
        raw_tables["martyrology"] = jsonpickle.decode(
            f.read(), classes=[datastructures.Date, datastructures.Martyrology]
        )


years = {}

year_tables = {"martyrology": None}
raw_tables = {}


def assemble_martyrology(candidates: list, year: int):
    """
    Assemble and resolve martyrolgy (easy, as we just stuff them together.)

    Parameters
    ----------
    candidates: list : candidates for the day.

    year: int : year.


    Returns
    -------
    old_date string and content list, with extra stuff tacked on top.
    """
    extra_info = []
    for candidate in candidates:
        try:
            old_date, content = candidate.render(year)
        except AttributeError:
            extra_info += candidate.content
    return old_date, extra_info + content


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
        return year_tables[table][year][day]
    except (KeyError, TypeError):
        this_year = eval_year(year, raw_tables[table])
        try:
            year_tables[table][year] = this_year
        except (KeyError, TypeError):
            year_tables[table] = {year: this_year}
        return year_tables[table][year][day]


def martyrology_query(day, table):
    candidates = raw_query(day, table)
    return assemble_martyrology(candidates, day.year)


def init():
    """Start database."""
    load_martyrology()
