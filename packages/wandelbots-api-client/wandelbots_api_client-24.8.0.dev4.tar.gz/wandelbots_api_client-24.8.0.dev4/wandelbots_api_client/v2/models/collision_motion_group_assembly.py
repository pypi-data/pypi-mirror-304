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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.v2.models.collider import Collider
from typing import Optional, Set
from typing_extensions import Self

class CollisionMotionGroupAssembly(BaseModel):
    """
    CollisionMotionGroupAssembly
    """ # noqa: E501
    stored_link_chain: Optional[StrictStr] = Field(default=None, description="References a stored link chain. ")
    stored_tool: Optional[StrictStr] = Field(default=None, description="References a stored tool. ")
    link_chain: Optional[List[Dict[str, Collider]]] = Field(default=None, description="A link chain is a kinematic chain of links that is connected via joints. A motion group can be used to control the motion of the joints in a link chain.  A link is a group of colliders that is attached to the link reference frame.  The reference frame of a link is obtained after applying all sets of Denavit-Hartenberg-parameters from base to (including) the link index.  This means that the reference frame of the link is on the rotation axis of the next joint in the kinematic chain. Example: For a motion group with 2 joints, the collider reference frame (CRF) for link 1 is on the rotation axis of joint 2. The chain looks like: - Origin >> Mounting >> Base >> (CRF Base) Joint 0 >> Link 0 >> (CRF Link 0) Joint 1 >> Link 1 >> (CRF Link 1) Flange (CRF Tool) >> TCP  Adjacent links in the kinematic chain of the motion group are not checked for mutual collision. ")
    tool: Optional[Dict[str, Collider]] = Field(default=None, description="Defines the shape of a tool.  A tool is a dictionary of colliders.  All colliders that make up a tool are attached to the flange frame of the motion group. ")
    __properties: ClassVar[List[str]] = ["stored_link_chain", "stored_tool", "link_chain", "tool"]

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
        """Create an instance of CollisionMotionGroupAssembly from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in link_chain (list)
        _items = []
        if self.link_chain:
            for _item in self.link_chain:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                _items.append({key: value.to_dict() for key, value in _item.items()})
                # <<< End modification
            _dict['link_chain'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in tool (dict)
        _field_dict = {}
        if self.tool:
            for _key in self.tool:
                if self.tool[_key]:
                    _field_dict[_key] = self.tool[_key].to_dict()
            _dict['tool'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CollisionMotionGroupAssembly from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "stored_link_chain": obj.get("stored_link_chain"),
            "stored_tool": obj.get("stored_tool"),
            "link_chain": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                {key: Collider.from_dict(value) for key, value in _item.items()} if isinstance(_item, dict) else _item
                # <<< End modification
                for _item in obj["link_chain"]
            ] if obj.get("link_chain") is not None else None,
            "tool": dict(
                (_k, Collider.from_dict(_v))
                for _k, _v in obj["tool"].items()
            )
            if obj.get("tool") is not None
            else None
        })
        return _obj


