import json
from pathlib import Path

import dateutil.parser as dp
import jsonpickle
from flask import Flask
from jinja2 import Environment, PackageLoader

from ..objects import datastructures  # needed for unpickling.
from ..objects.datastructures import *

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
    print(martyrology[0])


def json_query(day):
    old_date, martyrology = raw_query(day)
    return json.dumps({"old_date": old_date, "content": martyrology})


invalid_date = "<title>Invalid date supplied</title>"

api = Flask(__name__)


@api.route("/martyrology/<day>", methods=["GET"])
def html_query(day):
    try:
        day = dp.parse(day).date()
        print(day)
    except ValueError:
        return invalid_date

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
