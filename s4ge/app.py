import mistletoe

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from . import config

md_templated_source = Environment(loader=FileSystemLoader(config.SOURCE_PATH))

def render_md_templated(dependencies, targets):
    for dep, targ in zip(dependencies, targets):
        Path(targ).parent.mkdir(
            parents=True, exist_ok=True
        )  # Create dirs if doesn't exists
        with open(targ, "w") as destination:
            destination.write(
                md_templated_source.get_template(
                    str(Path(dep).relative_to(config.SOURCE_PATH))
                ).render(config=config.Configured)
            )


def render_md_to_html(dependencies, targets):
    for dep, targ in zip(dependencies, targets):
        Path(targ).parent.mkdir(
            parents=True, exist_ok=True
        )  # Create dirs if doesn't exists
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(mistletoe.markdown(source.read()))


def render_to_template(dependencies, targets, template):
    template = config.Templates.get_template(template)
    for dep, targ in zip(dependencies, targets):
        Path(targ).parent.mkdir(
            parents=True, exist_ok=True
        )  # Create dirs if doesn't exists
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(template.render({"content": source.read()})),
