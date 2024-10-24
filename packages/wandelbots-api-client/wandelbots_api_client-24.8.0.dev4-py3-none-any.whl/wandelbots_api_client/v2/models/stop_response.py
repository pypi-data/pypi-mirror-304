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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class StopResponse(BaseModel):
    """
    The response will be sent once at the end of every motion signalling that the motion group has stopped moving.
    """ # noqa: E501
    stop_code: StrictStr
    message: Optional[StrictStr] = Field(default=None, description="Will provide detailed information about the reason for stopping.")
    location_on_trajectory: Union[StrictFloat, StrictInt]
    __properties: ClassVar[List[str]] = ["stop_code", "message", "location_on_trajectory"]

    @field_validator('stop_code')
    def stop_code_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['STOP_CODE_UNKNOWN', 'STOP_CODE_USER_REQUEST', 'STOP_CODE_PATH_END', 'STOP_CODE_JOINT_LIMIT_REACHED', 'STOP_CODE_IO', 'STOP_CODE_FORCE_LIMIT', 'STOP_CODE_ERROR']):
            raise ValueError("must be one of enum values ('STOP_CODE_UNKNOWN', 'STOP_CODE_USER_REQUEST', 'STOP_CODE_PATH_END', 'STOP_CODE_JOINT_LIMIT_REACHED', 'STOP_CODE_IO', 'STOP_CODE_FORCE_LIMIT', 'STOP_CODE_ERROR')")
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
        """Create an instance of StopResponse from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of StopResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "stop_code": obj.get("stop_code"),
            "message": obj.get("message"),
            "location_on_trajectory": obj.get("location_on_trajectory")
        })
        return _obj


