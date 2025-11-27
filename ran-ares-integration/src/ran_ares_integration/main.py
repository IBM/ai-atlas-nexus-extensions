import os
import tempfile
from typing import Dict, List

import pandas as pd
import yaml
from ares.redteam import RedTeamer
from jinja2 import Template
from ai_atlas_nexus.ai_risk_ontology.datamodel.ai_risk_ontology import Risk
from ai_atlas_nexus.blocks.inference import InferenceEngine
from ai_atlas_nexus.toolkit.logging import configure_logger

from ran_ares_integration.assets import ASSETS_DIR_PATH, RISK_TO_ARES_MAPPING
from ran_ares_integration.datamodel.risk_to_ares_ontology import RiskToARESIntent
from ran_ares_integration.datamodel.target_connector_ontology import Connector
from ran_ares_integration.utils.prompt_templates import ARES_GOALS_TEMPLATE


logger = configure_logger(__name__)


def resolve_ares_assets_path(param_dict, assets_path):
    for param, param_value in param_dict.items():
        if isinstance(param_value, str) and param_value.lower().startswith("assets"):
            param_dict[param] = param_value.replace("assets", str(assets_path))
        elif isinstance(param_value, Dict):
            resolve_ares_assets_path(param_value, assets_path)


def generate_attack_seeds(risk, inference_engine):
    return inference_engine.generate(
        prompts=[
            Template(ARES_GOALS_TEMPLATE).render(
                risk_name=risk.name,
                risk_description=risk.description,
                risk_concern=risk.concern,
            )
        ],
        response_format={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                },
                "required": ["prompt"],
            },
        },
        postprocessors=["json_object"],
        verbose=False,
    )[0].prediction


class Extension:

    def __init__(self, inference_engine: InferenceEngine, target: Connector):
        """Main extension class to run the task

        Args:
            inference_engine (InferenceEngine): An instance of the LLM inference engine
            target (Connector): A target AI model to perform the ARES red-teaming evaluation
        """
        self.inference_engine = inference_engine
        self.target = target

    def run(self, risk: Risk):
        """Submit potential attack risks for ARES red-teaming evaluation

        Args:
            risks (List[Risk]):
                A List of attack risks

        Returns:
            None
        """

        # filter risk_to_ares mappings for the given risk
        risk_to_ares_intents: List[RiskToARESIntent] = list(
            filter(
                lambda mapping: mapping.risk_id == risk.tag,
                RISK_TO_ARES_MAPPING.mappings,
            )
        )

        if len(risk_to_ares_intents) == 1:
            ares_intent = risk_to_ares_intents[0].intent

            logger.info(f"ARES mapping found for risk: {risk.name}")

            logger.info(f"Generating attack seeds...")
            attack_seeds = generate_attack_seeds(risk, self.inference_engine)
            logger.info(f"No. of attack seeds generated: {len(attack_seeds)}")

            # Write ARES attack seeds to a tmp file system
            attack_seeds_path = os.path.join(tempfile.gettempdir(), "attack_seeds.csv")
            pd.DataFrame(attack_seeds).rename(
                columns={"prompt": ares_intent.goal.goal}
            ).to_csv(attack_seeds_path, index=False)

            # replace ARES assests path wherever applicable
            ares_intent = ares_intent.model_dump(by_alias=True)
            resolve_ares_assets_path(ares_intent, ASSETS_DIR_PATH)

            # Call ARES RedTeamer API for evaluation
            try:
                rt = RedTeamer(
                    user_config={
                        "target": {
                            self.target.name: self.target.model_dump(by_alias=True)
                        },
                        "red-teaming": {
                            "intent": ares_intent["name"],
                            "prompts": attack_seeds_path,
                        },
                        ares_intent["name"]: ares_intent,
                    },
                    connectors=yaml.safe_load(
                        ASSETS_DIR_PATH.joinpath("connectors.yaml").read_text()
                    )["connectors"],
                    verbose=False,
                )
                rt.redteam(False, -1)
            except Exception as e:
                print(str(e))
                return
        else:
            raise Exception(f"ARES mapping not available for: {risk.name}")
