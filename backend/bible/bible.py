import re

from dotmap import DotMap


class Bible:
    def __init__(self, version: str):
        self.version = version
        self.content = DotMap()

    def _parse_ref(self, ref: str):
        """Convert ref into book, chapter and verse."""
        book, chapter, verse = re.search(r"([0-9]*.+?)([0-9]+):([0-9]+)", ref).groups()
        chapter = int(chapter)
        verse = int(verse)
        return book, chapter, verse

    def get_range(self, start: str, end: str = None):
        """Get all verses between start and end."""
        start_ref = self._parse_ref(start)
        book, chapter, verse = start_ref
        end_ref = (
            self._parse_ref(end)
            if end
            else (book, chapter, list(self.content[book][chapter].keys())[-1])
        )
        verses = []
        current_ref = start_ref

        print(start_ref, end_ref)
        if end_ref:
            while True:
                book, chapter, verse = current_ref
                chapter = int(chapter)
                verse = int(verse)
                verses.append(self.content[book][chapter][verse])
                if current_ref == end_ref:
                    break

                if verse + 1 in self.content[book][chapter].keys():
                    current_ref = (book, chapter, verse + 1)
                elif chapter + 1 in self.content[book].keys():
                    current_ref = (book, chapter + 1, 1)
                else:
                    current_ref = (books[books.index(book) + 1], 1, 1)

        return verses


books = [
    "Gn",
    "Ex",
    "Lev",
    "Num",
    "Dt",
    "Jos",
    "Jdc",
    "Ru",
    "1Reg",
    "2Reg",
    "3Reg",
    "4Reg",
    "1Par",
    "2Par",
    "Esd",
    "Neh",
    "Tb",
    "Jdt",
    "Est",
    "Jb",
    "Ps",
    "Pr",
    "Qo",
    "Ct",
    "Sap",
    "Si",
    "Is",
    "Jer",
    "Lam",
    "Ba",
    "Ez",
    "Dn",
    "Os",
    "Jl",
    "Am",
    "Ab",
    "Jon",
    "Mi",
    "Na",
    "Ha",
    "So",
    "Ag",
    "Za",
    "Mal",
    "1Ma",
    "2Ma",
    "Mt",
    "Mc",
    "Lc",
    "Jo",
    "Ac",
    "Rm",
    "1Co",
    "2Co",
    "Ga",
    "Ep",
    "Ph",
    "Col",
    "1Th",
    "2Th",
    "1Tim",
    "2Tim",
    "Tit",
    "Phm",
    "He",
    "Jc",
    "1Pe",
    "2Pe",
    "1Jo",
    "2Jo",
    "3Jo",
    "Judæ",
    "Ap",
]
