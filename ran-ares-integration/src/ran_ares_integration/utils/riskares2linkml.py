"""
This file creates a LinkML schema using the current mappings between ARES and Risk Atlas Nexus.
The goal is to update these mappings whenever new ones become available and are approved for
introduction into Risk Atlas Nexus.
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


risk_to_ares = pd.read_csv(ASSETS_DIR_PATH.joinpath("mappings/risk_to_ares.csv"))
goals = pd.read_csv(ASSETS_DIR_PATH.joinpath("mappings/goals.csv"))
strategies = pd.read_csv(ASSETS_DIR_PATH.joinpath("mappings/strategies.csv"))
evaluations = pd.read_csv(ASSETS_DIR_PATH.joinpath("mappings/evaluations.csv"))

mappings = []
for row in risk_to_ares.itertuples():
    goal = goals[goals["id"] == row.goal_id].iloc[0].to_dict()
    strategy = strategies[strategies["id"].isin(row.strategy_ids.split(","))]
    evaluation = evaluations[evaluations["id"] == row.evaluation_id].iloc[0].to_dict()
    mappings.append(
        RiskToARESIntent(
            id=row.id,
            name=row.name,
            risk_id=row.risk_id,
            intent=AresIntent(
                id=str(uuid4()),
                name=f"Ares_Intent_{row.risk_id}",
                goal=ARESGoal(**goal),
                strategy={
                    ares_strategy["id"]: ARESStrategy(
                        output_path=f"results/{ares_strategy["id"]}_output.json",
                        **{
                            x: y
                            for x, y in ares_strategy.to_dict().items()
                            if y != pd.NA
                        },
                    )
                    for _, ares_strategy in strategy.iterrows()
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
