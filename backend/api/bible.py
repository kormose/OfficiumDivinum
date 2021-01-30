from flask import request
from flask_api.decorators import set_renderers
from flask_api.renderers import (
    BaseRenderer,
    BrowsableAPIRenderer,
    JSONRenderer,
)

from ..bible import Vulgate
from .api import api

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
        book = args["book"]
        chapter = str(args["chapter"])
        verseno = str(args["verse"])
        verse = bible.content[book][chapter][verseno]
        return [verse]

    else:
        print(query)

        bible = versions[query["version"]]
        if not bible.content:
            bible.load()
        verses = []
        for book, chapter, verse in query["verses"]:
            chapter = str(chapter)
            verse = str(verse)
            verses.append(bible.content[book][chapter][verse])
        return verses
