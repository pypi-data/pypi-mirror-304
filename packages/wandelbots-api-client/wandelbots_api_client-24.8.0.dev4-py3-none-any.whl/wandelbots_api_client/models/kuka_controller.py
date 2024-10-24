# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.kuka_controller_rsi_server import KukaControllerRsiServer
from typing import Optional, Set
from typing_extensions import Self

class KukaController(BaseModel):
    """
    The configuration of a physical KUKA robot controller has to contain an IP address. Additionally an RSI server configuration has to be specified in order to control the robot. Deploying the server is a functionality of this API. 
    """ # noqa: E501
    kind: Optional[StrictStr] = 'KukaController'
    controller_ip: StrictStr = Field(alias="controllerIp")
    controller_port: StrictInt = Field(alias="controllerPort")
    rsi_server: KukaControllerRsiServer = Field(alias="rsiServer")
    __properties: ClassVar[List[str]] = ["kind", "controllerIp", "controllerPort", "rsiServer"]

    @field_validator('kind')
    def kind_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['KukaController']):
            raise ValueError("must be one of enum values ('KukaController')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of KukaController from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of rsi_server
        if self.rsi_server:
            _dict['rsiServer'] = self.rsi_server.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KukaController from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "kind": obj.get("kind") if obj.get("kind") is not None else 'KukaController',
            "controllerIp": obj.get("controllerIp"),
            "controllerPort": obj.get("controllerPort") if obj.get("controllerPort") is not None else 54600,
            "rsiServer": KukaControllerRsiServer.from_dict(obj["rsiServer"]) if obj.get("rsiServer") is not None else None
        })
        return _obj


