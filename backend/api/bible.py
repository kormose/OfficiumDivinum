from flask import abort, request
from flask_api.decorators import set_renderers
from flask_api.renderers import (
    BaseRenderer,
    BrowsableAPIRenderer,
    JSONRenderer,
)

from ..bible import Vulgate
from .api import api

# from .errors import InvalidInput

versions = {"vulgate": Vulgate("Sixto-Clementine Vulgate")}


class objectHTMLRenderer(BaseRenderer):
    media_type = 'text/html; charset="UTF-8"'

    def render(self, data, media_type, **options):

        rendered = ""
        for thing in data:
            rendered += thing.html()

        else:
            return rendered


@api.route("/bible/", methods=["Get"])
@set_renderers(JSONRenderer, objectHTMLRenderer, BrowsableAPIRenderer)
def get_verses():

    query = request.get_json()
    if not query:
        args = request.args
        bible = versions[args["version"]]
        if not bible.content:
            bible.load()

        try:
            start = args["start"]
            end = args["end"] if "end" in args.keys() else None
            verses = bible.get_range(start, end)
            return verses

        except Exception:
            abort(400)

    else:
        print(query)

        bible = versions[query["version"]]
        if not bible.content:
            bible.load()
        verses = []
        try:
            for book, chapter, verse in query["verses"]:
                chapter = chapter
                verse = verse
                verses.append(bible.content[book][chapter][verse])
        except KeyError:
            pass

        try:
            start = query["start"]
            end = query["end"] if "end" in query.keys() else None
            verses += bible.get_range(start, end)
        except KeyError:
            pass

        if not verses:
            abort(400)

        return verses
