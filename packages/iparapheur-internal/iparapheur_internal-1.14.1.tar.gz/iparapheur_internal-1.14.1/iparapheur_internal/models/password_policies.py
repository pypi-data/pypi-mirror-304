# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class PasswordPolicies(BaseModel):
    """
    PasswordPolicies
    """ # noqa: E501
    min_length: Optional[StrictInt] = Field(default=None, alias="minLength")
    max_length: Optional[StrictInt] = Field(default=None, alias="maxLength")
    not_username: Optional[StrictBool] = Field(default=None, alias="notUsername")
    not_email: Optional[StrictBool] = Field(default=None, alias="notEmail")
    special_chars_min_count: Optional[StrictInt] = Field(default=None, alias="specialCharsMinCount")
    uppercase_chars_min_count: Optional[StrictInt] = Field(default=None, alias="uppercaseCharsMinCount")
    lowercase_chars_min_count: Optional[StrictInt] = Field(default=None, alias="lowercaseCharsMinCount")
    digits_min_count: Optional[StrictInt] = Field(default=None, alias="digitsMinCount")
    regex_pattern: Optional[StrictStr] = Field(default=None, alias="regexPattern")
    __properties: ClassVar[List[str]] = ["minLength", "maxLength", "notUsername", "notEmail", "specialCharsMinCount", "uppercaseCharsMinCount", "lowercaseCharsMinCount", "digitsMinCount", "regexPattern"]

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
        """Create an instance of PasswordPolicies from a JSON string"""
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
        """Create an instance of PasswordPolicies from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "minLength": obj.get("minLength"),
            "maxLength": obj.get("maxLength"),
            "notUsername": obj.get("notUsername"),
            "notEmail": obj.get("notEmail"),
            "specialCharsMinCount": obj.get("specialCharsMinCount"),
            "uppercaseCharsMinCount": obj.get("uppercaseCharsMinCount"),
            "lowercaseCharsMinCount": obj.get("lowercaseCharsMinCount"),
            "digitsMinCount": obj.get("digitsMinCount"),
            "regexPattern": obj.get("regexPattern")
        })
        return _obj


