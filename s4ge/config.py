from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json

APP_DIR = Path(__file__).resolve(strict=True).parent
PROJECT_DIR = APP_DIR.parent

# In the future we'll look for different extensions
with (PROJECT_DIR / "_config.json").open() as ff:
    Configured = json.load(ff)

SOURCE_PATH = PROJECT_DIR / Configured["source"]
INTERMEDIARY_PATH = PROJECT_DIR / Configured["rendered"]
DESTINATION_PATH = PROJECT_DIR / Configured["destination"]

Templates = Environment(loader=FileSystemLoader(PROJECT_DIR / Configured["templates"]))
