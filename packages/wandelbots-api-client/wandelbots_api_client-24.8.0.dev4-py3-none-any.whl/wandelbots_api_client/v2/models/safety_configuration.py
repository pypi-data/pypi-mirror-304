# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 2.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.v2.models.geometry import Geometry
from wandelbots_api_client.v2.models.planning_limits import PlanningLimits
from wandelbots_api_client.v2.models.robot_link_geometry import RobotLinkGeometry
from wandelbots_api_client.v2.models.safety_zone import SafetyZone
from wandelbots_api_client.v2.models.safety_zone_limits import SafetyZoneLimits
from typing import Optional, Set
from typing_extensions import Self

class SafetyConfiguration(BaseModel):
    """
    The safety configuration of a motion-group. Used for motion planning.
    """ # noqa: E501
    global_limits: PlanningLimits
    safety_zone_limits: Optional[List[SafetyZoneLimits]] = Field(default=None, description="All limits applied in certain SafetyZones.")
    safety_zones: Optional[List[SafetyZone]] = Field(default=None, description="SafetyZones are areas which cannot be entered or impose certain limits.")
    robot_model_geometries: Optional[List[RobotLinkGeometry]] = Field(default=None, description="The shape of the motion-group to validate against SafetyZones.")
    tcp_geometries: Optional[List[Geometry]] = Field(default=None, description="The shape of the TCP to validate against SafetyZones.")
    __properties: ClassVar[List[str]] = ["global_limits", "safety_zone_limits", "safety_zones", "robot_model_geometries", "tcp_geometries"]

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
        """Create an instance of SafetyConfiguration from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of global_limits
        if self.global_limits:
            _dict['global_limits'] = self.global_limits.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in safety_zone_limits (list)
        _items = []
        if self.safety_zone_limits:
            for _item in self.safety_zone_limits:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['safety_zone_limits'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in safety_zones (list)
        _items = []
        if self.safety_zones:
            for _item in self.safety_zones:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['safety_zones'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in robot_model_geometries (list)
        _items = []
        if self.robot_model_geometries:
            for _item in self.robot_model_geometries:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['robot_model_geometries'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tcp_geometries (list)
        _items = []
        if self.tcp_geometries:
            for _item in self.tcp_geometries:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['tcp_geometries'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SafetyConfiguration from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "global_limits": PlanningLimits.from_dict(obj["global_limits"]) if obj.get("global_limits") is not None else None,
            "safety_zone_limits": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                SafetyZoneLimits.from_dict(_item) if hasattr(SafetyZoneLimits, 'from_dict') else _item
                # <<< End modification
                for _item in obj["safety_zone_limits"]
            ] if obj.get("safety_zone_limits") is not None else None,
            "safety_zones": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                SafetyZone.from_dict(_item) if hasattr(SafetyZone, 'from_dict') else _item
                # <<< End modification
                for _item in obj["safety_zones"]
            ] if obj.get("safety_zones") is not None else None,
            "robot_model_geometries": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                RobotLinkGeometry.from_dict(_item) if hasattr(RobotLinkGeometry, 'from_dict') else _item
                # <<< End modification
                for _item in obj["robot_model_geometries"]
            ] if obj.get("robot_model_geometries") is not None else None,
            "tcp_geometries": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                Geometry.from_dict(_item) if hasattr(Geometry, 'from_dict') else _item
                # <<< End modification
                for _item in obj["tcp_geometries"]
            ] if obj.get("tcp_geometries") is not None else None
        })
        return _obj


