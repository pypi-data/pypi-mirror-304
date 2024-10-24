# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel, Field, constr

class AsAtPredicateContract(BaseModel):
    """
    AsAtPredicateContract
    """
    value: Optional[constr(strict=True, max_length=25, min_length=5)] = None
    date_time_offset: Optional[datetime] = Field(None, alias="dateTimeOffset")
    __properties = ["value", "dateTimeOffset"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AsAtPredicateContract:
        """Create an instance of AsAtPredicateContract from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if value (nullable) is None
        # and __fields_set__ contains the field
        if self.value is None and "value" in self.__fields_set__:
            _dict['value'] = None

        # set to None if date_time_offset (nullable) is None
        # and __fields_set__ contains the field
        if self.date_time_offset is None and "date_time_offset" in self.__fields_set__:
            _dict['dateTimeOffset'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AsAtPredicateContract:
        """Create an instance of AsAtPredicateContract from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AsAtPredicateContract.parse_obj(obj)

        _obj = AsAtPredicateContract.parse_obj({
            "value": obj.get("value"),
            "date_time_offset": obj.get("dateTimeOffset")
        })
        return _obj
