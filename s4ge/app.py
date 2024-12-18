import mistletoe
import yaml

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from . import config



def _load_front_matter(dep, dep_root, fm_root):
    front_matter = {}
    fm = Path(
        fm_root,
        Path(dep).relative_to(dep_root).with_suffix(".yaml"),
    )
    if fm.is_file():
        with open(fm) as ffm:
            front_matter = yaml.safe_load(ffm)
    return front_matter


def pop_front_matter(dependencies, targets):
    dependencies.sort()
    targets.sort()
    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        with (
            open(dep) as source,
            open(targ, "w") as destination,
        ):
            # Buffer front-matter
            write_cur = False
            front_matter = ""
            cur = source.readline()  # First line - skip if no front matter
            print(cur)
            if cur.rstrip() != "---":
                write_cur = True
            else:
                cur = source.readline()
                while cur.rstrip() != "---":
                    print(cur)
                    front_matter += cur
                    cur = source.readline()

            # Write front-matter if any
            if front_matter.strip() != "":
                with Path(targ).with_suffix(".yaml").open("w") as dest_yaml:
                    dest_yaml.write(front_matter)

            # Write first line if no front-matter
            if write_cur:
                destination.write(cur)
            # Write remaining source
            destination.write(source.read())


def render_md_templated(dependencies, targets, dep_root):
    dependencies.sort()
    targets.sort()

    md_templated_source = Environment(loader=FileSystemLoader(dep_root))

    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        # Load front-matter
        front_matter = _load_front_matter(dep, dep_root, dep_root)

        with open(targ, "w") as destination:
            destination.write(
                md_templated_source.get_template(
                    str(Path(dep).relative_to(dep_root))
                ).render(
                    {
                        "config": config.Configured,
                        "page": front_matter,
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


def render_to_template(dependencies, targets, dep_root, frontmatter_root):
    dependencies.sort()
    targets.sort()
    for dep, targ in zip(dependencies, targets):
        # Create target parents if it doesn't exist
        Path(targ).parent.mkdir(parents=True, exist_ok=True)

        # Load front matter and template if any
        front_matter = _load_front_matter(dep, dep_root, frontmatter_root)
        fm_template_name = front_matter.get("layout", None)

        # Get config for current file
        cur_conf = config.Configured["values"]
        template_name = fm_template_name
        for part in Path(dep).relative_to(dep_root).parts:
            try:
                cur_conf = cur_conf[part]

                # Skip if layout defined in front-matter
                if fm_template_name is not None:
                    continue
                try:
                    template_name = cur_conf["layout"]
                except KeyError:
                    continue
            except KeyError:
                break

        # Default template
        if template_name is None:
            template_name = config.Configured["layout"]
        # Write rendered
        with open(dep) as source, open(targ, "w") as destination:
            destination.write(
                config.Templates.get_template(template_name).render(
                    {
                        "content": source.read(),
                        "config": config.Configured,
                        "page": front_matter,
                    }
                )
            )
