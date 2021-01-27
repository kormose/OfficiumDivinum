#!/usr/bin/python3
"""Parse Divinumofficium's calendar tabulae into feast object."""

from pathlib import Path

from ..DSL import months
from ..objects import (
    Celebration,
    Commemoration,
    Date,
    Feast,
    Rank,
    rank_table_by_calendar,
)


def parse_line(line: str, calendar) -> Feast:
    line = line.strip()
    if line.startswith("*"):
        return None
    rank_table = rank_table_by_calendar[calendar]

    parts = line.split("=")
    date, duplicate_date, name, rank = parts[:4]
    try:
        rank = Rank(rank_table[int(rank)])
    except ValueError:
        rank = Rank(rank_table[int(float(rank) + 0.5)], defeatable=True)

    commemorations = None
    if len(parts) > 5 and parts[4]:
        commemorations = []
        commemoration_rank = None
        for part in parts[4:]:
            try:
                commemoration_rank = float(part)
                try:
                    commemoration_rank = Rank(rank_table[int(part)])
                except ValueError:
                    commemoration_rank = Rank(
                        rank_table[int(float(part) + 0.5)],
                        defeatable=True,
                    )
                break
            except ValueError:
                commemorations.append(part)

        commemorations = [Commemoration(x, commemoration_rank) for x in commemorations]

    qualifiers = None
    if date != duplicate_date:
        qualifiers = duplicate_date[:-1]

    month, day = (int(x) for x in date.split("-"))
    if day == 0:
        Type = "de Tempore"
        datestr = "Sun between 2 Jan 5 Jan OR 2 Jan"
    else:
        Type = "Sanctorum"
        datestr = f"{day} {months[month - 1]}"
    return Feast(
        rank,
        Date(datestr),
        calendar,
        Type,
        celebration=Celebration(name),
        commemorations=commemorations,
        qualifiers=qualifiers,
    )


def parse_file(fn: Path, calendar: str):
    year = []

    with fn.open() as f:
        for line in f.readlines():
            parsed = parse_line(line, calendar)
            if parsed:
                year.append(parsed)

    return year


if __name__ == "__main__":
    print(
        "Do not run this parser directly.  A helper script is ../run_parser.py, or use it in a python shell"
    )
