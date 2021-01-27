import re
from pathlib import Path
from typing import Union

from ..DSL import days, months, ordinals, specials
from ..objects import Date, Martyrology, MartyrologyInfo
from .T2obj import parse_DO_sections

christ_the_king_datestr = "Sat between 23 Oct 31 Oct"


def parse_file(fn: Path) -> Union[Martyrology, list[MartyrologyInfo]]:
    """
    Parse Martyrology file.

    Parameters
    ----------
    fn: Path : file to parse.


    Returns
    -------
    Martyrology object with rule for specific day.
    """
    if fn.stem == "Mobile":
        return parse_mobile_file(fn)

    month, day = (int(i) for i in fn.stem.split("-"))
    datestr = f"{day} {months[month - 1]}"
    content = []

    with fn.open() as f:
        old_date = f.readline().strip()
        f.readline()
        for line in f.readlines():
            content.append(line.strip())

    return Martyrology(Date(datestr), old_date, content)


def parse_mobile_file(fn: Path) -> list[MartyrologyInfo]:
    """
    Parse Martyrology 'Mobile' file.

    Parameters
    ----------
    fn: Path : mobile file to parse.


    Returns
    -------
    List of Martyrology objects with rules, which can be applied.
    """
    sections = parse_DO_sections(fn.readlines())

    mobile = []

    for datestr, section in sections.items():
        try:
            special, week, day = re.search(r"(.+)([0-9]+)-([0-9])", datestr).group(
                1, 2, 3
            )
            datestr = f"{ordinals[week]} {days[day]} after {specials[special]}"
        except IndexError:
            if datestr == "Nativity":  # hard coded elsewhere.
                continue
            elif datestr == "10-DU":
                datestr = christ_the_king_datestr
            elif datestr == "Defuncti":
                datestr = "2 Nov"

            mobile.append(MartyrologyInfo(Date(datestr), section))
    return mobile
