import os
import mistletoe
from pathlib import Path

from config import *

## Render Markdown (mistletoe)
def render_md_to_html(source_dir: Path, destination_dir: Path):
    for root, _dirs, filenames in os.walk(source_dir):
        for fname in filenames:
            source = Path(root, fname)

            if (not source.is_file() or
                not Path(fname).suffix in ("markdown", "md")):
                continue

            destination = Path(root.replace(source_dir.name, destination_dir.name, 1))
            destination.mkdir(parents=True, exist_ok=True)

            destination = destination / fname.with_suffix("html")

            with (
                source.open() as fin,
                destination.open("w") as fout,
            ):
                fout.write(
                    mistletoe.markdown(
                        fin.read()
                    )
                )

render_md_to_html(SOURCE, CONFIG["rendered"])


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
