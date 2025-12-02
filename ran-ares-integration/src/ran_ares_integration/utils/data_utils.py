import yaml


def read_yaml(yaml_path: str):
    with open(yaml_path) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise Exception(str(exc))
