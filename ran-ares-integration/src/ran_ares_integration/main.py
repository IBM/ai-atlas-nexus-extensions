import os
import tempfile
from typing import Dict, List

import pandas as pd
from ai_atlas_nexus.ai_risk_ontology.datamodel.ai_risk_ontology import Risk
from ai_atlas_nexus.blocks.inference import InferenceEngine
from ai_atlas_nexus.toolkit.logging import configure_logger
from ares.redteam import RedTeamer
from jinja2 import Template

import ran_ares_integration.mapper as mapper
from ran_ares_integration.assets import (
    ARES_CONNECTORS,
    ASSETS_DIR_PATH,
    load_ares_mappings,
)
from ran_ares_integration.datamodel.risk_to_ares_ontology import (
    RiskToARESIntent,
    RiskToARESMapping,
)
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

    def __init__(self, inference_engine: InferenceEngine, target: Dict):
        """Main extension class to run the task

        Args:
            inference_engine (InferenceEngine): An instance of the LLM inference engine
            target (Connector): A target AI model to perform the ARES red-teaming evaluation
        """
        self.inference_engine = inference_engine
        self.target = target

    def generate_mapping(self, risk: Risk) -> Dict:
        return mapper.generate(risk, self.inference_engine)

    def update_mapping(self, ares_config: Dict) -> RiskToARESMapping:
        return mapper.update(ares_config)

    def run(self, risk: Risk, auto_update_mapping=False) -> None:
        """Submit potential attack risks for ARES red-teaming evaluation

        Args:
            risk (Risk):
                An AI Atals Nexus risk to start ARES evaluation
            auto_update_mapping (bool, optional): Whether to update ARES mappings automatically
                if the given risk is not present. Defaults to False.
        """

        # filter risk_to_ares mappings for the given risk
        risk_to_ares_intents: List[RiskToARESIntent] = list(
            filter(
                lambda mapping: mapping.risk_id == risk.id,
                load_ares_mappings().mappings,
            )
        )

        if len(risk_to_ares_intents) == 0:
            if not auto_update_mapping:
                raise Exception(
                    f"ARES mapping not available for risk: {risk.name}. To enable automatic ARES mapping, please re-run with the `auto_update_mapping` flag set to True."
                )
            else:
                logger.warning(
                    f"ARES mapping not available for: {risk.name}. Preparing to update ARES mapping before starting evaluation..."
                )
                ares_config = self.generate_mapping(risk)
                mappings = self.update_mapping(ares_config)
                logger.warning(
                    f"Generated mapping added to the current python environment. Please ask the extension owner if you want the mapping to be permanently added to the extension."
                )

                # search again after the update
                risk_to_ares_intents: List[RiskToARESIntent] = list(
                    filter(lambda mapping: mapping.risk_id == risk.id, mappings)
                )

                if len(risk_to_ares_intents) == 0:
                    raise Exception("ARES mapping update failed.")

        ares_intent = risk_to_ares_intents[0].intent

        logger.info(f"ARES mapping found for risk: {risk.name}")

        # logger.info(f"Generating attack seeds...")
        attack_seeds = generate_attack_seeds(risk, self.inference_engine)
        logger.info(f"No. of attack seeds generated: {len(attack_seeds)}")

        # Write ARES attack seeds to a tmp file system
        attack_seeds_path = os.path.join(tempfile.gettempdir(), "attack_seeds.csv")
        pd.DataFrame(attack_seeds).rename(
            columns={"prompt": ares_intent.goal.goal}
        ).to_csv(attack_seeds_path, index=False)

        # replace ARES assests path wherever applicable
        ares_intent = ares_intent.model_dump(exclude_none=True, exclude_unset=True)
        resolve_ares_assets_path(ares_intent, ASSETS_DIR_PATH)

        # Call ARES RedTeamer API for evaluation
        try:
            rt = RedTeamer(
                user_config={
                    "target": {self.target["name"]: self.target},
                    "red-teaming": {
                        "intent": ares_intent["name"],
                        "prompts": attack_seeds_path,
                    },
                    ares_intent["name"]: ares_intent,
                },
                connectors=ARES_CONNECTORS,
                verbose=False,
            )
            rt.redteam(False, -1)
        except Exception as e:
            print(str(e))
            return
