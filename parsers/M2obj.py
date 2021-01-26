from pathlib import Path

from ..DSL import months
from ..objects import Date, Martyrology


def parse_file(fn: Path) -> Martyrology:
    """Parse Martyrology file."""
    month, day = (int(i) for i in fn.stem.split("-"))
    datestr = f"{day} {months[month - 1]}"
    content = []

    with fn.open() as f:
        old_date = f.readline().strip()
        f.readline()
        for line in f.readlines():
            content.append(line.strip())

    return Martyrology(Date(datestr), old_date, content)
