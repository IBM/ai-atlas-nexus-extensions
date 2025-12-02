from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


metamodel_version = "None"
version = "0.0.1"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="allow",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_curi_maps": ["semweb_context"],
        "default_prefix": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors/",
        "default_range": "string",
        "description": "Vocabulary to integrate Ares workflow",
        "id": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors",
        "imports": ["linkml:types", "common"],
        "name": "ares",
        "prefixes": {
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            }
        },
        "source_file": "ran-ares-integration/src/ran_ares_integration/schema/target_connector.yaml",
    }
)


class Entity(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "abstract": True,
            "class_uri": "schema:Thing",
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/common",
        }
    )

    id: str = Field(
        default=...,
        description="""A unique identifier to this instance of the model element. Example identifiers include UUID, URI, URN, etc.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Entity"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""A text name of this instance.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Entity", "HuggingFaceConnector"],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""The description of an entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Entity"],
                "slot_uri": "schema:description",
            }
        },
    )
    url: Optional[str] = Field(
        default=None,
        description="""An optional URL associated with this instance.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "url",
                "domain_of": ["Entity"],
                "slot_uri": "schema:url",
            }
        },
    )
    dateCreated: Optional[date] = Field(
        default=None,
        description="""The date on which the entity was created.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "dateCreated",
                "domain_of": ["Entity"],
                "slot_uri": "schema:dateCreated",
            }
        },
    )
    dateModified: Optional[date] = Field(
        default=None,
        description="""The date on which the entity was most recently modified.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "dateModified",
                "domain_of": ["Entity"],
                "slot_uri": "schema:dateModified",
            }
        },
    )


class Connector(Entity):
    """
    The target large language model (LLM) for conducting the ARES red-teaming evaluation.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    id: str = Field(
        default=...,
        description="""A unique identifier to this instance of the model element. Example identifiers include UUID, URI, URN, etc.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Entity"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""A text name of this instance.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Entity", "HuggingFaceConnector"],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""The description of an entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Entity"],
                "slot_uri": "schema:description",
            }
        },
    )
    url: Optional[str] = Field(
        default=None,
        description="""An optional URL associated with this instance.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "url",
                "domain_of": ["Entity"],
                "slot_uri": "schema:url",
            }
        },
    )
    dateCreated: Optional[date] = Field(
        default=None,
        description="""The date on which the entity was created.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "dateCreated",
                "domain_of": ["Entity"],
                "slot_uri": "schema:dateCreated",
            }
        },
    )
    dateModified: Optional[date] = Field(
        default=None,
        description="""The date on which the entity was most recently modified.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "dateModified",
                "domain_of": ["Entity"],
                "slot_uri": "schema:dateModified",
            }
        },
    )


class HuggingFaceConnector(Connector):
    """
    The target large language model (LLM) for conducting the ARES red-teaming evaluation.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    type: str = Field(
        default="ares.connectors.huggingface.HuggingFaceConnector",
        description="""String describing the python type""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": ["HuggingFaceConnector"],
                "ifabsent": "ares.connectors.huggingface.HuggingFaceConnector",
            }
        },
    )
    name: Optional[str] = Field(
        default="huggingface",
        description="""name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Entity", "HuggingFaceConnector"],
                "ifabsent": "huggingface",
            }
        },
    )
    seed: Optional[int] = Field(
        default=42,
        description="""Seed to be applied to model, for example, 42.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "seed",
                "domain_of": ["HuggingFaceConnector"],
                "ifabsent": "42",
            }
        },
    )
    device: Optional[str] = Field(
        default="auto",
        description="""Device on which to load the model, for example, 'auto'.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "device",
                "domain_of": ["HuggingFaceConnector"],
                "ifabsent": "auto",
            }
        },
    )
    model_configs: ModelConfig = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "model_configs",
                "domain_of": ["HuggingFaceConnector"],
            }
        },
    )
    tokenizer_config: TokenizerConfig = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "tokenizer_config",
                "domain_of": ["HuggingFaceConnector"],
            }
        },
    )
    generate_kwargs: Optional[GenerateKwargs] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "generate_kwargs",
                "domain_of": ["HuggingFaceConnector"],
            }
        },
    )
    prompt_path: Optional[str] = Field(
        default=None,
        description="""The evaluator prompt path.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prompt_path",
                "domain_of": ["HuggingFaceConnector"],
            }
        },
    )
    id: str = Field(
        default=...,
        description="""A unique identifier to this instance of the model element. Example identifiers include UUID, URI, URN, etc.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Entity"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""The description of an entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Entity"],
                "slot_uri": "schema:description",
            }
        },
    )
    url: Optional[str] = Field(
        default=None,
        description="""An optional URL associated with this instance.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "url",
                "domain_of": ["Entity"],
                "slot_uri": "schema:url",
            }
        },
    )
    dateCreated: Optional[date] = Field(
        default=None,
        description="""The date on which the entity was created.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "dateCreated",
                "domain_of": ["Entity"],
                "slot_uri": "schema:dateCreated",
            }
        },
    )
    dateModified: Optional[date] = Field(
        default=None,
        description="""The date on which the entity was most recently modified.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "dateModified",
                "domain_of": ["Entity"],
                "slot_uri": "schema:dateModified",
            }
        },
    )


class ModelConfig(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    pretrained_model_name_or_path: str = Field(
        default="Qwen/Qwen2-0.5B-Instruct",
        description="""pretrained_model_name_or_path""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "pretrained_model_name_or_path",
                "domain_of": ["ModelConfig", "TokenizerConfig"],
                "ifabsent": "Qwen/Qwen2-0.5B-Instruct",
            }
        },
    )
    torch_dtype: Optional[str] = Field(
        default="bfloat16",
        description="""model_config""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "torch_dtype",
                "domain_of": ["ModelConfig"],
                "ifabsent": "bfloat16",
            }
        },
    )


class TokenizerConfig(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    pretrained_model_name_or_path: str = Field(
        default="Qwen/Qwen2-0.5B-Instruct",
        description="""pretrained_model_name_or_path""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "pretrained_model_name_or_path",
                "domain_of": ["ModelConfig", "TokenizerConfig"],
                "ifabsent": "Qwen/Qwen2-0.5B-Instruct",
            }
        },
    )
    padding_side: Optional[str] = Field(
        default="left",
        json_schema_extra={
            "linkml_meta": {
                "alias": "padding_side",
                "domain_of": ["TokenizerConfig"],
                "ifabsent": "left",
            }
        },
    )


class GenerateKwargs(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    chat_template: Optional[ChatTemplate] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "chat_template", "domain_of": ["GenerateKwargs"]}
        },
    )
    generate_params: Optional[GenerateParams] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "generate_params", "domain_of": ["GenerateKwargs"]}
        },
    )


class ChatTemplate(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    return_tensors: Optional[str] = Field(
        default="pt",
        json_schema_extra={
            "linkml_meta": {
                "alias": "return_tensors",
                "domain_of": ["ChatTemplate"],
                "ifabsent": "pt",
            }
        },
    )
    thinking: Optional[bool] = Field(
        default=True,
        json_schema_extra={
            "linkml_meta": {
                "alias": "thinking",
                "domain_of": ["ChatTemplate"],
                "ifabsent": "True",
            }
        },
    )
    return_dict: Optional[bool] = Field(
        default=True,
        json_schema_extra={
            "linkml_meta": {
                "alias": "return_dict",
                "domain_of": ["ChatTemplate"],
                "ifabsent": "True",
            }
        },
    )
    add_generation_prompt: Optional[bool] = Field(
        default=True,
        json_schema_extra={
            "linkml_meta": {
                "alias": "add_generation_prompt",
                "domain_of": ["ChatTemplate"],
                "ifabsent": "True",
            }
        },
    )


class GenerateParams(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors"
        }
    )

    max_new_tokens: Optional[int] = Field(
        default=50,
        json_schema_extra={
            "linkml_meta": {
                "alias": "max_new_tokens",
                "domain_of": ["GenerateParams"],
                "ifabsent": "50",
            }
        },
    )


class TargetConnectors(ConfiguredBaseModel):
    """
    An umbrella object that holds mapping instances of Connector.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://ibm.github.io/ran-ares-integration/ontology/target_connectors",
            "tree_root": True,
        }
    )

    connectors: list[HuggingFaceConnector] = Field(
        default=...,
        description="""A list of connector""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "connectors",
                "any_of": [{"range": "HuggingFaceConnector"}],
                "domain_of": ["TargetConnectors"],
            }
        },
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Entity.model_rebuild()
Connector.model_rebuild()
HuggingFaceConnector.model_rebuild()
ModelConfig.model_rebuild()
TokenizerConfig.model_rebuild()
GenerateKwargs.model_rebuild()
ChatTemplate.model_rebuild()
GenerateParams.model_rebuild()
TargetConnectors.model_rebuild()
