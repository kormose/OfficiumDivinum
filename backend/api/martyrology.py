from datetime import datetime, timedelta

import dateutil.parser as dp
from flask import jsonify, request
from jinja2 import Environment, PackageLoader

from . import database
from .api import api

env = Environment(loader=PackageLoader("backend.api", "template/html/"))
martyrology_template = env.get_template("martyrology.html")


def init():
    database.init()


def json_query(day, table):
    old_date, martyrology = database.martyrology_query(day, table)
    return jsonify({"old_date": old_date, "content": martyrology})


invalid_date = "<title>Invalid date supplied</title>"


@api.route("/martyrology/", methods=["GET"])
def get_martyrology():
    args = request.args
    print(args)
    try:
        day = dp.parse(args["date"])
    except KeyError:
        day = datetime.now() + timedelta(days=1)
    day = day.date()

    try:
        if args["type"] == "json":
            return json_query(day, "martyrology")
    except KeyError:
        pass
    return html_query(day, "martyrology")


# @api.route("/jsonapi", methods=["GET"])
# def json_api_query():
#     query = request.get_json()
#     if query["request"] == "martyrology"


def html_query(day, table):
    old_date, content = database.martyrology_query(day, table)
    args = {"old_date": old_date, "content": content}
    return martyrology_template.render(**args)


def main():
    init()
    print(dir(api))
    print(api)
    api.run()


if __name__ == "__main__":
    main()
