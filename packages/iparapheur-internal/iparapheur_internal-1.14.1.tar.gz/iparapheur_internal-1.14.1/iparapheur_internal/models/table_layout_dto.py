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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from iparapheur_internal.models.labelled_column import LabelledColumn
from iparapheur_internal.models.table_name import TableName
from typing import Optional, Set
from typing_extensions import Self

class TableLayoutDto(BaseModel):
    """
    TableLayoutDto
    """ # noqa: E501
    id: Optional[StrictStr] = None
    table_name: Optional[TableName] = Field(default=None, alias="tableName")
    default_asc: Optional[StrictBool] = Field(default=None, alias="defaultAsc")
    default_sort_by: Optional[StrictStr] = Field(default=None, alias="defaultSortBy")
    column_list: Optional[List[StrictStr]] = Field(default=None, alias="columnList")
    labelled_column_list: Optional[List[LabelledColumn]] = Field(default=None, alias="labelledColumnList")
    __properties: ClassVar[List[str]] = ["id", "tableName", "defaultAsc", "defaultSortBy", "columnList", "labelledColumnList"]

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
        """Create an instance of TableLayoutDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "labelled_column_list",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in labelled_column_list (list)
        _items = []
        if self.labelled_column_list:
            for _item_labelled_column_list in self.labelled_column_list:
                if _item_labelled_column_list:
                    _items.append(_item_labelled_column_list.to_dict())
            _dict['labelledColumnList'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TableLayoutDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "tableName": obj.get("tableName"),
            "defaultAsc": obj.get("defaultAsc"),
            "defaultSortBy": obj.get("defaultSortBy"),
            "columnList": obj.get("columnList"),
            "labelledColumnList": [LabelledColumn.from_dict(_item) for _item in obj["labelledColumnList"]] if obj.get("labelledColumnList") is not None else None
        })
        return _obj


