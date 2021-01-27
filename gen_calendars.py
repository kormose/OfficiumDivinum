from pathlib import Path

from backend.parsers.run_parser import pokemon_to_json

things = list(
    pokemon_to_json(
        "Latin", "1960", "~/code/office-generator/divinumofficium/DO_web/www/horas"
    )
)

fns = ("sanctoral", "temporal", "martyrology")

root = Path("./backend/api")

for i in range(len(fns)):
    with (root / f"{fns[i]}.json").open("w") as f:
        f.write(things[i])
