from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering
from typing import List, Union

import pylunar

from ..DSL import dsl_parser
from .divinumofficium_structures import (
    feria_ranks,
    latin_feminine_ordinals,
    new_rank_table,
    traditional_rank_lookup_table,
    typo_translations,
)
from .html_render import verse_template

"""
Since sometimes we call parsers manually, we enforce only parsing for
calendars for which we have built Calendar() objects, otherwise we
wouldn't know what to do with the generated data.
"""
valid_calendars = [
    "1955",
    "1960",
]  # list of valid calendars. Might need an object list instead.  Or perhaps don't check and rely on in

"""Valid types of day."""
valid_day_types = ["de Tempore", "Sanctorum"]


class RankException(Exception):
    """"""


Rank = None  # temporary var to allow circular classing....


@dataclass
class Octave:
    """Class to represent an octave, which may be of various kinds
    rank: rank of the octave."""

    name: str
    privileged: bool = None
    rank: Rank = None


@dataclass
class Rank:
    """
    Class to represent the rank of a particular feast.

    This must be
    able to return a machine-readable and sortable object (we use an
    integer from 0 with 0 = feria) and also preserve the particular
    name we use in any given calendar .

    Parameters
    ----------

    Returns
    -------
    """

    name: str = "Feria"
    defeatable: bool = None
    octave: Octave = None

    def __post_init__(self):
        try:
            self.name = typo_translations[self.name]
        except KeyError:
            pass

        name = self.name.strip().lower()
        if (
            name not in traditional_rank_lookup_table.keys()
            and name not in new_rank_table
            and name not in feria_ranks.keys()
        ):
            raise RankException(f"Rank {self.name} not valid")

    def _to_int(self):
        """"""
        name = self.name.strip().lower()
        try:
            val = traditional_rank_lookup_table[name]
        except ValueError:
            try:
                val = new_rank_table.index(name)
            except ValueError:
                return feria_ranks[name]
        return val if not self.defeatable else val - 0.1


class CalendarException(Exception):
    """"""


@dataclass
class Commemoration:
    """
    A class to represent a commemoration.

    This might be a bit more in depth than we need to go.

    Parameters
    ----------

    Returns
    -------
    """

    name: str
    rank: Rank


@dataclass
class Celebration:
    """
    A class to represent a celebration.

    This might be a bit more in depth than we need to go.

    Parameters
    ----------

    Returns
    -------
    """

    name: str


@dataclass
class Date:
    """
    A class to represent a date which may or may not need resolving for a specific year.

    Parameters
    ----------

    Returns
    -------
    """

    rules: str
    date: datetime = None

    def resolve(self, year: int):
        """

        Parameters
        ----------
        year: int :


        Returns
        -------

        """
        self.date = dsl_parser(self.rules, year)
        return self.date


@total_ordering
@dataclass
class Feast:
    """
    Object to represent a liturgical day.

    These are sortable by rank, although sorting objects with distinct
    calendars is unsupported and will probably return nonsense.

    Multiple Feast objects can meaningfully exist for a given calendar
    day, if they have different `Type`s.  (I.e. tempore/sanctorum.)
    This might be a design decision worth re-thinking down the line.

    Parameters
    ----------

    Returns
    -------
    """

    rank: Rank
    date: Union[datetime, Date]
    calendar: str
    Type: str
    name: str = None
    celebration: Celebration = None
    commemorations: List = None
    qualifiers: List = None  # for matching things up in DO's weird system

    def __post_init__(self):
        """Check constraints."""
        self.calendar = str(self.calendar)
        if self.calendar not in valid_calendars:
            raise CalendarException(
                f"Invalid calendar supplied {self.calendar}, "
                f"valid are {valid_calendars}"
            )

        if self.Type not in valid_day_types:
            raise CalendarException(
                f"Invalid Type supplied {self.Type}, " f"valid are {valid_day_types}"
            )

        if not self.name and self.celebration:
            self.name = self.celebration.name

    def __lt__(self, other):
        return self.rank._to_int() < other.rank._to_int()

    def __eq__(self, other):
        return self.rank._to_int() == other.rank._to_int()


@dataclass
class Feria:
    """Class to represent a feria, which can be quite a complicated thing."""

    name: str

    def _to_int(self):
        """"""
        return feria_ranks[self.name]


@dataclass
class MartyrologyInfo:
    """Class to represent a martyrology entry which should be appended after the date
    and before the content fixed for the day."""

    date: Date
    content: List


@dataclass
class Martyrology:
    """Class to represent the martyrology for a given day."""

    date: Date
    old_date: str
    content: List
    ordinals: List = None
    moonstr: str = " Luna {ordinal} Anno Domini {year}"

    def __post_init__(self):
        if not self.ordinals:
            self.ordinals = latin_feminine_ordinals

    def lunar(self, date: datetime):
        """

        Parameters
        ----------
        date: datetime :


        Returns
        -------

        """
        m = pylunar.MoonInfo((31, 46, 19), (35, 13, 1))  # lat/long Jerusalem
        m.update((date.year, date.month, date.day, 0, 0, 0))
        age = round(m.age())
        return age

    def render(self, year: int):
        """

        Parameters
        ----------
        year: int :


        Returns
        -------

        """
        date = self.date.resolve(year)
        ordinal = self.ordinals[self.lunar(date) - 1]
        old_date = self.old_date + self.moonstr.format(
            ordinal=ordinal.title(), year=year
        )
        # may need to abstract this to handle translations
        return old_date, self.content


@dataclass
class Verse:
    """"""

    number: int
    chapter: int
    book: str
    content: str
    version: str = None  # in case we want it later

    def html(self):
        """Return html rendered."""
        return verse_template.render(v=self)


@dataclass
class Reading:
    """"""

    name: str
    ref: str
    content: List[Union[Verse, str]]
    description: str = None


@dataclass
class Responsory:
    """
    Class to represent a responsory.

    Later we may want to make this more explicit.

    Parameters
    ----------

    Returns
    -------
    """

    content: List[str]


@dataclass
class Collect:
    """Class to represent a collect."""

    collect: str
    termination: str


@dataclass
class Rules:
    """"""

    source: Feast = None
    nocturns: int = None
    sunday_psalms: bool = None
    antiphons_at_hours: bool = None
    proper_hymns: List[str] = None
    Te_Deum: bool = None
    skip_psalm_93 = None
    lessons: int = None
    doxology: str = None
    feria: bool = None
    festum_Domini: bool = None
    gloria_responsory: bool = None
    vespers_antiphons: List[str] = None
    second_chapter_verse: bool = None
    second_chapter_verse_lauds: bool = None
    commemoration_key: int = None
    duplex: bool = None
    hymn_terce: bool = None
    crossref: Feast = None
    one_antiphon: bool = None
    athanasian_creed: bool = None
    stjamesrule: str = None
    psalm_5_vespers: int = None
    psalm_5_vespers_3: int = None
    initia_cum_responsory: bool = None
    invit2: bool = None
    laudes2: bool = None
    laudes_litania: bool = None
    first_lesson_saint: bool = None
    limit_benedictiones_oratio: bool = None
    minores_sine_antiphona: bool = None
    no_commemoration: bool = None
    no_suffragium: bool = None
    no_commemoration_sunday: bool = None
    omit: List = None
    sunday_collect: bool = None
    preces_feriales: bool = None
    proper: bool = None
    psalm_53_prime: bool = None
    psalmi_minores_dominica: bool = None
