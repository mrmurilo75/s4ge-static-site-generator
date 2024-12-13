import mistletoe

from pathlib import Path

from . import config


def render_md_to_html(dependencies, targets):
    for dep, targ in zip(dependencies, targets):
        Path(targ).parent.mkdir(parents=True, exist_ok=True)  # Create dirs if doesn't exists
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(mistletoe.markdown(source.read()))


def render_to_template(dependencies, targets, template):
    template = config.Templates.get_template(template)
    for dep, targ in zip(dependencies, targets):
        Path(targ).parent.mkdir(parents=True, exist_ok=True)  # Create dirs if doesn't exists
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(template.render({"content": source.read()})),
