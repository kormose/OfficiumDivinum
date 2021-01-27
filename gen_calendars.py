from backend.parsers.run_parser import pokemon_to_json

sanctoral, temporal, martyrology = pokemon_to_json(
    "Latin", "1960", "~/code/office-generator/divinumofficium/DO_web/www/horas"
)

with open("sanctoral.json", "w") as f:
    f.write(sanctoral)

with open("temporal.json", "w") as f:
    f.write(temporal)

with open("martyrology.json", "w") as f:
    f.write(martyrology)
