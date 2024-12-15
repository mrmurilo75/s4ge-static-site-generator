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


def render_to_template(dependencies, targets, dep_root):
    for dep, targ in zip(dependencies, targets):
        # Get config for current file
        cur_conf = config.Configured["values"]
        template_name = config.Configured["layout"]
        for part in Path(dep).relative_to(dep_root).parts:
            try:
                cur_conf = cur_conf[part]
                try:
                    template_name = cur_conf["layout"]
                except KeyError:
                    continue
            except KeyError:
                break

        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        # Write rendered
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(
                config.Templates.get_template(template_name).render(
                    {"content": source.read()}
                )
            )
