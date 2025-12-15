from pathlib import Path

import yaml


def read_yaml(yaml_path: str):
    if not Path(yaml_path).exists():
        return None
    with open(yaml_path) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise Exception(str(exc))
