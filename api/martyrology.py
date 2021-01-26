from datetime import datetime, timedelta
from pathlib import Path

import dateutil.parser as dp
import jsonpickle
from flask import Flask, jsonify, request
from jinja2 import Environment, PackageLoader

from ..objects import datastructures  # needed for unpickling.

env = Environment(loader=PackageLoader("OfficiumDivinum.api", "template/html/"))
martyrology_template = env.get_template("martyrology.html")

martyrology = []


def eval_year(year, yearless, as_list=True):
    yeared = {}
    for row in yearless:
        if not row:
            continue
        date = row.date.resolve(year)
        if as_list:
            try:
                yeared[date].append(row)
            except KeyError:
                yeared[date] = [row]
        else:
            yeared[date] = row

    return yeared


def load_martyrology():
    global martyrology
    with Path("OfficiumDivinum/api/martyrology.json").open() as f:
        martyrology = jsonpickle.decode(
            f.read(), classes=[datastructures.Date, datastructures.Martyrology]
        )


years = {}


def raw_query(day):
    global years
    year = day.year
    try:
        return years[year][day].render(year)
    except KeyError:
        years[year] = eval_year(year, martyrology, False)
        return years[year][day].render(year)


def init():
    load_martyrology()


def json_query(day):
    old_date, martyrology = raw_query(day)
    return jsonify({"old_date": old_date, "content": martyrology})


invalid_date = "<title>Invalid date supplied</title>"

api = Flask(__name__)


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
            return json_query(day)
    except KeyError:
        pass
    return html_query(day)


def html_query(day):
    old_date, content = raw_query(day)
    args = {"old_date": old_date, "content": content}
    return martyrology_template.render(**args)


def main():
    init()
    print(dir(api))
    print(api)
    api.run()


if __name__ == "__main__":
    main()
