"""
This file creates a LinkML schema using the current mappings between ARES and AI Atlas Nexus.
The goal is to update these mappings whenever new ones become available and are approved for
introduction into AI Atlas Nexus.
"""

import os
from uuid import uuid4

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


risk_to_ares_map = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/risk_to_ares.yaml"))
goals = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/goals.yaml"))
strategies = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/strategies.yaml"))
evaluations = read_yaml(ASSETS_DIR_PATH.joinpath("mappings/evaluations.yaml"))

mappings = []
for risk_to_ares in risk_to_ares_map:
    goal = list(filter(lambda goal: goal["id"] == risk_to_ares["goal_id"], goals))[0]
    strategy = list(
        filter(
            lambda strategy: strategy["id"] in risk_to_ares["strategy_ids"], strategies
        )
    )
    evaluation = list(
        filter(
            lambda evaluation: evaluation["id"] == risk_to_ares["evaluation_id"],
            evaluations,
        )
    )[0]

    mappings.append(
        RiskToARESIntent(
            id=risk_to_ares["id"],
            risk_id=risk_to_ares["risk_id"],
            name=risk_to_ares["name"],
            intent=AresIntent(
                id=str(uuid4()),
                name=f"Ares_Intent_{risk_to_ares["name"]}",
                goal=ARESGoal(**goal),
                strategy={
                    ares_strategy["id"]: ARESStrategy(
                        output_path=f"results/{ares_strategy["id"]}_output.json",
                        **ares_strategy,
                    )
                    for ares_strategy in strategy
                },
                evaluation=AresEvaluator(
                    connector=(
                        risk_to_ares["evaluation_model"]
                        if "evaluation_model" in risk_to_ares
                        else None
                    ),
                    **evaluation,
                ),
            ),
        )
    )

with open(
    os.path.join(ASSETS_DIR_PATH, "knowledge_graph", "risk_to_ares_mappings_NEW.yaml"),
    "+tw",
    encoding="utf-8",
) as output_file:
    print(
        YAMLDumper().dumps(RiskToARESMapping(mappings=mappings)),
        file=output_file,
    )
