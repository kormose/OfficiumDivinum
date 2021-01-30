from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("backend.objects", "templates/"))

verse_template = env.get_template("verse.html")
