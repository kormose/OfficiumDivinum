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
