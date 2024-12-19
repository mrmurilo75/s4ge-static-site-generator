import mistletoe
import json
import yaml

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from . import config


def multilevel_dict_access(
    path: list[str],
    source: dict[str, any],
    access_key="_values",
    write: bool | dict = False,
    default=None,
):
    """
    Iterates over the nested dicts *source* by the *path* of keys. (A node is a level of nesting)
    If no optional arguments are passed, the values in each node are colleted and returned.
    If the *path* doesn't exist, returns *default*.

    The *access_key* is used to access the value of a node. If it has this key, it must return a dict. Defaults to '_values'.

    If *write* is a dict, it writes its value and the collected values to the leaf. Using True is the same as an empty dict.
    When writing, the values will only be in the leafs.
    """
    writing = write or isinstance(write, dict)
    if write is True:
        write = {}

    cur = source

    leaf_value = {}
    leaf_value.update(
        cur.get(access_key, {})
    )

    for part in path:
        if cur.get(part, None) is None:
            if not writing:
                return default
            cur[part] = {}

        cur = cur[part]
        leaf_value.update(cur.get(access_key, {}))

    if writing:
        leaf_value.update(write)
        cur[access_key] = leaf_value

    return leaf_value


def clean_source(dependencies, targets, dep_root, full_config):
    dependencies.sort()
    targets.sort()

    config_values = config.Configured["cascade"]

    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        with open(dep) as source, open(targ, "w") as destination:
            # Buffer front-matter
            write_first = False
            front_matter_str = ""
            front_matter = {}
            cur_line = source.readline()  # First line - skip if no front matter
            if cur_line.rstrip() != "---":
                write_first = True
            else:
                cur_line = source.readline()
                while cur_line.rstrip() != "---":
                    front_matter_str += cur_line
                    cur_line = source.readline()
                front_matter = yaml.safe_load(front_matter_str)

            # Write config and front_matter
            multilevel_dict_access(  # updates config_values
                Path(dep).with_suffix("").relative_to(dep_root).parts,
                config_values,
                write=front_matter,
            )
            with open(full_config, "w") as full_conf_file:
                json.dump(config_values, full_conf_file)

            # Write first line if no front-matter
            if write_first:
                destination.write(cur_line)
            # Write remaining source
            destination.write(source.read())


def render_md_templated(dependencies, targets, dep_root, full_config):
    dependencies.sort()
    targets.sort()

    md_templated_source = Environment(loader=FileSystemLoader(dep_root))

    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        with open(full_config) as full_config_file, open(targ, "w") as destination:
            pages_config = json.load(full_config_file)
            destination.write(
                md_templated_source.get_template(
                    str(Path(dep).relative_to(dep_root))
                ).render(
                    {
                        "config": config.Configured,
                        "pages": pages_config,
                        "page": multilevel_dict_access(
                            Path(dep).relative_to(dep_root).parts,
                            pages_config,
                        ),
                    }
                )
            )


def render_md_to_html(dependencies, targets):
    dependencies.sort()
    targets.sort()
    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        # Write html-ed
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(mistletoe.markdown(source.read()))


def render_to_template(dependencies, targets, dep_root, full_config):
    dependencies.sort()
    targets.sort()
    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        # Write rendered
        with (
            open(full_config) as full_config_file,
            open(dep) as source,
            open(targ, "w") as destination,
        ):
            pages_config = json.load(full_config_file)

            page = multilevel_dict_access(
                Path(dep).with_suffix("").relative_to(dep_root).parts,
                pages_config,
            )
            destination.write(
                config.Templates.get_template(page["layout"]).render(
                    {
                        "content": source.read(),
                        "config": config.Configured,
                        "pages": pages_config,
                        "page": page,
                    }
                )
            )
