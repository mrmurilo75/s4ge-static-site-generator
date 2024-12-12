from pathlib import Path
import json

APP_DIR = Path(__file__).resolve(strict=True).parent

# In the future we'll look for different extensions
with (APP_DIR / '_config.json').open("r") as ff:
    CONFIG = json.load(ff)

SOURCE_PATH = APP_DIR / CONFIG["source"]
DESTINATION_PATH = APP_DIR / CONFIG["destination"]
TEMPLATES_PATH = APP_DIR / CONFIG["templates"]
