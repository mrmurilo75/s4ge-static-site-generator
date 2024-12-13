import os

from pathlib import Path


def get_all_files(source_dir: str | Path, validate: callable = lambda s: True):
    result = set()
    for root, _dirs, filenames in os.walk(source_dir):
        root_path = Path(root)
        for fname in filenames:
            cur = root_path / fname
            if validate(cur):
                result.add(cur)
    return result


def is_markdown(source: Path):
    return source.is_file() and source.suffix in (".md", ".markdown")
