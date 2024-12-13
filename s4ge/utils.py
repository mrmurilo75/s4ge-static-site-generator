import os

from pathlib import Path


def get_all_files(
    source_dir: str | Path,
    validate: callable = lambda s: True,
    relative: bool = False,
):
    """
    Returns all paths filtered by 'validate'.
    If relative is set to True, the returned paths are relative to 'source_dir'. Otherwise, they are absolute.

    :validate: receives a Path and must return a booleable
    """
    result = []
    for root, _dirs, filenames in os.walk(source_dir):
        root_path = Path(root)
        result += (
            [root_path / fname for fname in filenames if validate(root_path / fname)]
            if not relative
            else [
                (root_path / fname).relative_to(source_dir)
                for fname in filenames
                if validate(root_path / fname)
            ]
        )
    return result


def replicate(paths: list[Path], target: Path, relative_to: Path | None = None):
    """
    Replicates a list of paths on a target directory.
    If 'relative_to' is given, it will replicate the paths relative to this directory.

    Assumes that 'relative_to' is a parent directory of paths.
    """
    return (
        [Path(target, path) for path in paths]
        if relative_to is None
        else [Path(target, path.relative_to(relative_to)) for path in paths]
    )


def is_markdown(source: Path):
    return source.is_file() and source.suffix in (".md", ".markdown")
