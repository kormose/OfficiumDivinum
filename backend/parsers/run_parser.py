#!/usr/bin/python3

from pathlib import Path

from jsonpickle import encode

from . import K2obj, M2obj, T2obj


def sanctoral_to_json(fn: Path, calendar: str):
    days = [K2obj.parse_file(fn, calendar)]
    print(encode(days, indent=2))


def martyrology_to_json(fn: Path):
    day = M2obj.parse_file(fn)
    print(encode(day, indent=2))


def temporal_to_json(fn: Path, calendar: str):
    day = T2obj.parse_file(fn, calendar)
    print(encode(day, indent=2))


def pokemon(lang, calendar, root):
    """Catch them all!"""
    sanctoral = K2obj.parse_file(
        Path(f"{root}/{lang}/Tabulae/K{calendar}.txt"),
        calendar,
    )
    temporal = []
    for f in Path(f"{root}/{lang}/Tempora").glob("*.txt"):
        temporal.append(T2obj.parse_file(f, calendar))

    martyrology = []
    for f in Path(f"{root}/{lang}/Martyrologium").glob("*.txt"):
        try:
            martyrology.append(M2obj.parse_file(f))
        except ValueError:
            pass
    return sanctoral, temporal, martyrology


def pokemon_to_json(lang, calendar, root):
    sanctoral, temporal, martyrology = pokemon(lang, calendar, root)
    print(encode(sanctoral))
    print(encode(temporal))
    print(encode(martyrology))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("INF", help="Input file.")
    parser.add_argument("--calendar", help="Select calendar.")
    actions = parser.add_argument_group("Actions")
    actions.add_argument("--martyrology", action="store_true")
    actions.add_argument("--sanctoral", action="store_true")
    actions.add_argument("--temporal", action="store_true")
    actions.add_argument("--pokemon", help="Get them all!  Supply lang.")

    args = parser.parse_args()
    if any([args.sanctoral, args.temporal]) and not args.calendar:
        raise Exception("Calendar needed")

    inf = Path(args.INF).expanduser()

    if args.sanctoral:
        sanctoral_to_json(inf, args.calendar)
    if args.martyrology:
        martyrology_to_json(inf)
    if args.temporal:
        temporal_to_json(inf, args.calendar)
    if args.pokemon:
        pokemon_to_json(args.pokemon, args.calendar, args.INF)
