import logging
import os
import mistletoe
from pathlib import Path

from s4ge.config import *


## Render Markdown (mistletoe)
def process_dir(
    source_path: Path,
    destination_path: Path,
    process: callable,
    source_validator: callable = lambda s: True,
    destination_transform: callable = lambda s: s,
):
    for root, _dirs, filenames in  os.walk(source_path):
        for source in filter(source_validator, (Path(root, fname) for fname in filenames)):
            destination_replica = destination_path / Path(source).relative_to(source_path)
            destination_replica.parent.mkdir(parents=True, exist_ok=True)

            destination = destination_transform(destination_replica)
            print(f"Processing source '{source}' to destination '{destination}'.")

            with (
                source.open() as fin,
                destination.open("w") as fout,
            ):
                process(fin, fout)


def render_md_to_html(source_dir, destination_dir):
    process_dir(
        source_dir,
        destination_dir,
        process = lambda source, destination: destination.write(mistletoe.markdown(source.read())),
        source_validator = lambda source: source.is_file() and source.suffix in (".markdown", ".md"),
        destination_transform = lambda destination: destination.with_suffix(".html"),
    )


## Render Jinja2 template
def render_to_template(source_dir, destination_dir, template):
    template = Templates.get_template(template)

    process_dir(
        source_dir,
        destination_dir,
        process = lambda s, d: d.write(template.render({"content": s.read()})),
    )
