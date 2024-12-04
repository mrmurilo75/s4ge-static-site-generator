## Render Markdown (mistletoe)
import mistletoe

SOURCE = '_source/index.md'
DESTINATION = '_rendered/index.html'

with open(SOURCE, 'r') as fin:
    rendered = mistletoe.markdown(fin)

with open(DESTINATION, 'w') as fout:  # Assumes folder exists
    fout.write(rendered)


## Render template (Jinja2)
from jinja2 import Environment, FileSystemLoader

SOURCE = '_rendered/index.html'
DESTINATION = '_site/index.html'

TEMPLATES_FOLDER = '_templates/'
TEMPLATE = 'index.html'

env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))
template = env.get_template(TEMPLATE)

context = {}
with open(SOURCE, 'r') as fin:
    context["content"] = fin.read()

rendered = template.render(context)

with open(DESTINATION, 'w') as fout:  # Assumes folder exists
    fout.write(rendered)
