# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class RotationAngleTypes(str, Enum):
    """
    The type of rotation description that is used to specify the rotation.  **Quaternion notation**  * The rotation is represented using a quaternion: [x, y, z, w]. * The vector part [x, y, z] is the imaginary part of the quaternion, and the scalar part [w] is the real part.  **Rotation Vector notation**  * The rotation is represented using an axis-angle representation: > axis = Vector[0:2] > angle = |axis| in [rad] > axis.normalized * angle  **Euler notation**  * *extrinsic* fixed external reference system * *intrinsic* reference system fixed to rotation body > angles = Vector[0:2] in [rad]. * ZYX, ZXZ,...   - mapping of the given angles values to the (either intrinsic     or extrinsic) axes in the stated order.  > Example ZYX: Z = Vector[0], Y = Vector[1], X = Vector[2]. 
    """

    """
    allowed enum values
    """
    QUATERNION = 'QUATERNION'
    ROTATION_VECTOR = 'ROTATION_VECTOR'
    EULER_ANGLES_INTRINSIC_ZXZ = 'EULER_ANGLES_INTRINSIC_ZXZ'
    EULER_ANGLES_INTRINSIC_XYX = 'EULER_ANGLES_INTRINSIC_XYX'
    EULER_ANGLES_INTRINSIC_YZY = 'EULER_ANGLES_INTRINSIC_YZY'
    EULER_ANGLES_INTRINSIC_ZYZ = 'EULER_ANGLES_INTRINSIC_ZYZ'
    EULER_ANGLES_INTRINSIC_XZX = 'EULER_ANGLES_INTRINSIC_XZX'
    EULER_ANGLES_INTRINSIC_YXY = 'EULER_ANGLES_INTRINSIC_YXY'
    EULER_ANGLES_INTRINSIC_XYZ = 'EULER_ANGLES_INTRINSIC_XYZ'
    EULER_ANGLES_INTRINSIC_YZX = 'EULER_ANGLES_INTRINSIC_YZX'
    EULER_ANGLES_INTRINSIC_ZXY = 'EULER_ANGLES_INTRINSIC_ZXY'
    EULER_ANGLES_INTRINSIC_XZY = 'EULER_ANGLES_INTRINSIC_XZY'
    EULER_ANGLES_INTRINSIC_ZYX = 'EULER_ANGLES_INTRINSIC_ZYX'
    EULER_ANGLES_INTRINSIC_YXZ = 'EULER_ANGLES_INTRINSIC_YXZ'
    EULER_ANGLES_EXTRINSIC_ZXZ = 'EULER_ANGLES_EXTRINSIC_ZXZ'
    EULER_ANGLES_EXTRINSIC_XYX = 'EULER_ANGLES_EXTRINSIC_XYX'
    EULER_ANGLES_EXTRINSIC_YZY = 'EULER_ANGLES_EXTRINSIC_YZY'
    EULER_ANGLES_EXTRINSIC_ZYZ = 'EULER_ANGLES_EXTRINSIC_ZYZ'
    EULER_ANGLES_EXTRINSIC_XZX = 'EULER_ANGLES_EXTRINSIC_XZX'
    EULER_ANGLES_EXTRINSIC_YXY = 'EULER_ANGLES_EXTRINSIC_YXY'
    EULER_ANGLES_EXTRINSIC_ZYX = 'EULER_ANGLES_EXTRINSIC_ZYX'
    EULER_ANGLES_EXTRINSIC_XZY = 'EULER_ANGLES_EXTRINSIC_XZY'
    EULER_ANGLES_EXTRINSIC_YXZ = 'EULER_ANGLES_EXTRINSIC_YXZ'
    EULER_ANGLES_EXTRINSIC_YZX = 'EULER_ANGLES_EXTRINSIC_YZX'
    EULER_ANGLES_EXTRINSIC_XYZ = 'EULER_ANGLES_EXTRINSIC_XYZ'
    EULER_ANGLES_EXTRINSIC_ZXY = 'EULER_ANGLES_EXTRINSIC_ZXY'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RotationAngleTypes from a JSON string"""
        return cls(json.loads(json_str))


