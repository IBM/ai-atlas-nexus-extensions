import os
from pathlib import Path

from linkml_runtime.loaders import yaml_loader

from ran_ares_integration.datamodel.risk_to_ares_ontology import RiskToARESMapping
from ran_ares_integration.utils.data_utils import read_yaml


ASSETS_DIR_PATH = Path(__file__).parent.absolute()

RISK_TO_ARES_MAPPING: RiskToARESMapping = yaml_loader.load_any(
    source=yaml_loader.load_as_dict(
        source=os.path.join(
            ASSETS_DIR_PATH, "knowledge_graph", "risk_to_ares_mappings.yaml"
        )
    ),
    target_class=RiskToARESMapping,
)

ARES_CONNECTORS = read_yaml(ASSETS_DIR_PATH.joinpath("connectors.yaml"))["connectors"]
