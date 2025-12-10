"""
This file creates a LinkML schema using the current mappings between ARES and AI Atlas Nexus.
The goal is to update these mappings whenever new ones become available and are approved for
introduction into AI Atlas Nexus.
"""

import json
import os
from importlib.resources import files
from pathlib import Path
from uuid import uuid4

import ares
import pandas as pd
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


risk_to_ares_configs = read_yaml(
    ASSETS_DIR_PATH.joinpath("mappings/risk_to_ares_configs.yaml")
)
ares_goals = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/goals.yaml"))
ares_strategies = json.loads(files(ares).joinpath("strategies.json").read_text())
ares_evaluations = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/evaluations.yaml"))


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


mappings = []
for risk_to_ares in risk_to_ares_configs:
    goal = parse_ares_components(risk_to_ares["goal"], ares_goals)
    strategies = dict(
        filter(
            lambda strategy: strategy[0] in risk_to_ares["strategy"],
            ares_strategies.items(),
        )
    )
    evaluation = parse_ares_components(risk_to_ares["evaluation"], ares_evaluations)

    mappings.append(
        RiskToARESIntent(
            id=str(uuid4()),
            risk_id=risk_to_ares["risk_id"],
            intent=AresIntent(
                id=str(uuid4()),
                name=f"{risk_to_ares["risk_name"].replace(" ","_")}-Ares_Intent",
                goal=ARESGoal(**goal),
                strategy={
                    strategy_name: parse_strategy_params(strategy_params)
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
        YAMLDumper().dumps(RiskToARESMapping(mappings=mappings)),
        file=output_file,
    )
