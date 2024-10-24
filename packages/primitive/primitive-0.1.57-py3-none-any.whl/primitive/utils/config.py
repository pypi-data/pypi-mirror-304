import json
from pathlib import Path
from typing import Dict

HOME_DIRECTORY = Path.home()
PRIMITIVE_CREDENTIALS_FILEPATH = Path(
    HOME_DIRECTORY / ".config" / "primitive" / "credentials.json"
)


def create_directory(filepath: Path = PRIMITIVE_CREDENTIALS_FILEPATH):
    filepath.mkdir(parents=True, exist_ok=True)


def create_config_file(filepath: Path = PRIMITIVE_CREDENTIALS_FILEPATH):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.touch()
    with filepath.open("w") as json_file:
        json.dump({}, json_file)


def update_config_file(
    filepath: Path = PRIMITIVE_CREDENTIALS_FILEPATH, new_config: Dict = {}
):
    existing_config = read_config_file(filepath=filepath)
    merged_config = {**existing_config, **new_config}
    with filepath.open("w") as json_file:
        json.dump(merged_config, json_file, indent=2)


def read_config_file(filepath: Path = PRIMITIVE_CREDENTIALS_FILEPATH) -> Dict:
    if not filepath.exists():
        create_config_file(filepath=filepath)
    return json.loads(filepath.read_text())
