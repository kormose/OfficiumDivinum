from flask import request
from flask_api.decorators import set_renderers
from flask_api.renderers import (
    BaseRenderer,
    BrowsableAPIRenderer,
    JSONRenderer,
)
from jinja2 import Environment, PackageLoader

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


#
# api.config["DEFAULT_RENDERERS"] = [JSONRenderer]


@api.route("/bible/", methods=["Get"])
# @set_renderers(objectHTMLRenderer, BrowsableAPIRenderer)  # JSONRenderer,
@set_renderers(objectHTMLRenderer)
def get_verses():

    query = request.get_json()
    if not query:
        args = request.args
        bible = versions[args["version"]]
        if not bible.content:
            print("loading")
            bible.load()
        book = args["book"]
        chapter = str(args["chapter"])
        verseno = str(args["verse"])
        verse = bible.content[book][chapter][verseno]
        return [verse]

    bible = versions[query["version"]]
    if not bible.content:
        bible.load()

    verses = query["verses"]
    if "nostyle" not in args.keys():
        response = page_css.render()
    else:
        response = ""
    for book, chapter, verse in verses:
        response += bible.book[chapter][verse].html()

    return response
