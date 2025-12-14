"""
This file updates an Risk to ARES configs using the current mappings between ARES and AI Atlas Nexus.
The goal is to update these mappings whenever new ones become available and are approved for
introduction into AI Atlas Nexus.
"""

import json
import os
from importlib.resources import files
from typing import Dict
from uuid import uuid4

import ares
import yaml
from ai_atlas_nexus.ai_risk_ontology.datamodel.ai_risk_ontology import Risk
from ai_atlas_nexus.blocks.inference import InferenceEngine
from ai_atlas_nexus.toolkit.logging import configure_logger
from jinja2 import Template
from linkml_runtime.dumpers import YAMLDumper

from ran_ares_integration.assets import ASSETS_DIR_PATH
from ran_ares_integration.datamodel.risk_to_ares_ontology import (
    AresEvaluator,
    ARESGoal,
    AresIntent,
    ARESStrategy,
    RiskToARESIntent,
    RiskToARESMapping,
)
from ran_ares_integration.utils.data_utils import read_yaml
from ran_ares_integration.utils.prompt_templates import ARES_SELECT_STRATEGIES_TEMPLATE


logger = configure_logger(__name__)

RISK_TO_ARES_CONFIGS = read_yaml(
    ASSETS_DIR_PATH.joinpath("mappings/risk_to_ares_configs.yaml")
)
ARES_GOALS = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/goals.yaml"))
ARES_STRATEGIES = json.loads(files(ares).joinpath("strategies.json").read_text())
ARES_EVALUATION = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/evaluations.yaml"))


def parse_ares_components(component, master_list):
    if isinstance(component, str):
        return next(filter(lambda master: master["id"] == component, master_list))
    elif isinstance(component, list):
        parsed_components = []
        for component_item in component:
            parsed_components.append(parse_ares_components(component_item, master_list))
        return parsed_components
    elif isinstance(component, dict):
        for component_id, component_params in component.items():
            parsed_component = next(
                filter(lambda master: master["id"] == component_id, master_list)
            )
            break
        return parsed_component | component_params


def parse_strategy_params(strategy_params):
    strategy_params["id"] = str(uuid4())
    for strategy_param_key, strategy_param_value in strategy_params.items():
        if strategy_param_key in ["input_path", "output_path"]:
            strategy_params[strategy_param_key] = strategy_param_value.replace(
                "assets", "results"
            )

    return strategy_params


def generate(
    risk: Risk, inference_engine: InferenceEngine, taxonomy: str = "ibm-risk-atlas"
) -> Dict:
    strategies = inference_engine.generate(
        prompts=[
            Template(ARES_SELECT_STRATEGIES_TEMPLATE).render(
                risk_name=risk.name,
                risk_description=risk.description,
                strategies=json.dumps(
                    [
                        {
                            "strategy_id": strategy_id,
                            "description": strategy["description"],
                        }
                        for strategy_id, strategy in ARES_STRATEGIES.items()
                    ],
                    indent=2,
                ),
            )
        ],
        response_format={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "strategy_id": {
                        "type": "string",
                        "enum": list(ARES_STRATEGIES.keys()),
                    },
                    "explanation": {"type": "string"},
                },
                "required": ["strategy_id", "explanation"],
            },
        },
        postprocessors=["json_object"],
        verbose=False,
    )[0].prediction

    NEW_CONFIG = {
        "risk_id": risk.id,
        "risk_name": risk.name,
        "goal": "generic_attack_goal",
        "strategy": [strategy["strategy_id"] for strategy in strategies[0:1]],
        "evaluation": "keyword",
    }

    logger.info(
        f"New ARES mapping generated: {json.dumps(NEW_CONFIG, indent=2)}.\nPlease run update() to add the new mapping to existing mappings."
    )

    return NEW_CONFIG


def update(risk_to_ares_config: Dict) -> RiskToARESMapping:

    RISK_TO_ARES_CONFIGS.append(risk_to_ares_config)
    with open(
        os.path.join(ASSETS_DIR_PATH, "mappings", "risk_to_ares_configs.yaml"), "w"
    ) as file:
        yaml.safe_dump(RISK_TO_ARES_CONFIGS, file, default_flow_style=False)

    mappings = []
    for risk_to_ares in RISK_TO_ARES_CONFIGS:
        goal = parse_ares_components(risk_to_ares["goal"], ARES_GOALS)
        strategies = dict(
            filter(
                lambda strategy: strategy[0] in risk_to_ares["strategy"],
                ARES_STRATEGIES.items(),
            )
        )
        evaluation = parse_ares_components(risk_to_ares["evaluation"], ARES_EVALUATION)

        mappings.append(
            RiskToARESIntent(
                id=str(uuid4()),
                risk_id=risk_to_ares["risk_id"],
                intent=AresIntent(
                    id=str(uuid4()),
                    name=f"{risk_to_ares["risk_name"].replace(" ","_")}-Ares_Intent",
                    goal=ARESGoal(**goal),
                    strategy={
                        strategy_name: ARESStrategy(
                            **parse_strategy_params(strategy_params)
                        )
                        for strategy_name, strategy_params in strategies.items()
                    },
                    evaluation=AresEvaluator(**evaluation),
                ),
            )
        )

    with open(
        os.path.join(ASSETS_DIR_PATH, "knowledge_graph", "risk_to_ares_mappings.yaml"),
        "+tw",
        encoding="utf-8",
    ) as output_file:
        print(
            YAMLDumper().dumps(RiskToARESMapping(mappings=mappings)), file=output_file
        )

    logger.info(f"Risk to ARES mappings succesfully updated.")

    return mappings
