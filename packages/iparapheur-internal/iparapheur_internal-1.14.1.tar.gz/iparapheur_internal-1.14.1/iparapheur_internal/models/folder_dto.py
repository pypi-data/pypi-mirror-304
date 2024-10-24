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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from iparapheur_internal.models.desk_representation import DeskRepresentation
from iparapheur_internal.models.document_dto import DocumentDto
from iparapheur_internal.models.signature_proof import SignatureProof
from iparapheur_internal.models.subtype_dto import SubtypeDto
from iparapheur_internal.models.task import Task
from iparapheur_internal.models.type_dto import TypeDto
from typing import Optional, Set
from typing_extensions import Self

class FolderDto(BaseModel):
    """
    FolderDto
    """ # noqa: E501
    id: Optional[StrictStr] = None
    name: Annotated[str, Field(min_length=2, strict=True, max_length=255)]
    due_date: Optional[datetime] = Field(default=None, alias="dueDate")
    metadata: Optional[Dict[str, StrictStr]] = None
    draft_creation_date: Optional[datetime] = Field(default=None, alias="draftCreationDate")
    type: Optional[TypeDto] = None
    subtype: Optional[SubtypeDto] = None
    origin_desk: Optional[DeskRepresentation] = Field(default=None, alias="originDesk")
    final_desk: Optional[DeskRepresentation] = Field(default=None, alias="finalDesk")
    is_read_by_current_user: Optional[StrictBool] = Field(default=None, alias="isReadByCurrentUser")
    legacy_id: Optional[StrictStr] = Field(default=None, alias="legacyId")
    type_id: Optional[StrictStr] = Field(default=None, alias="typeId")
    subtype_id: Optional[StrictStr] = Field(default=None, alias="subtypeId")
    step_list: Optional[List[Task]] = Field(default=None, alias="stepList")
    document_list: Optional[List[DocumentDto]] = Field(default=None, alias="documentList")
    signature_proof_list: Optional[List[SignatureProof]] = Field(default=None, alias="signatureProofList")
    read_by_user_ids: Optional[List[StrictStr]] = Field(default=None, alias="readByUserIds")
    read_by_current_user: Optional[StrictBool] = Field(default=None, alias="readByCurrentUser")
    __properties: ClassVar[List[str]] = ["id", "name", "dueDate", "metadata", "draftCreationDate", "type", "subtype", "originDesk", "finalDesk", "isReadByCurrentUser", "legacyId", "typeId", "subtypeId", "stepList", "documentList", "signatureProofList", "readByUserIds", "readByCurrentUser"]

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
        """Create an instance of FolderDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "draft_creation_date",
            "is_read_by_current_user",
            "step_list",
            "document_list",
            "signature_proof_list",
            "read_by_user_ids",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of type
        if self.type:
            _dict['type'] = self.type.to_dict()
        # override the default output from pydantic by calling `to_dict()` of subtype
        if self.subtype:
            _dict['subtype'] = self.subtype.to_dict()
        # override the default output from pydantic by calling `to_dict()` of origin_desk
        if self.origin_desk:
            _dict['originDesk'] = self.origin_desk.to_dict()
        # override the default output from pydantic by calling `to_dict()` of final_desk
        if self.final_desk:
            _dict['finalDesk'] = self.final_desk.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in step_list (list)
        _items = []
        if self.step_list:
            for _item_step_list in self.step_list:
                if _item_step_list:
                    _items.append(_item_step_list.to_dict())
            _dict['stepList'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in document_list (list)
        _items = []
        if self.document_list:
            for _item_document_list in self.document_list:
                if _item_document_list:
                    _items.append(_item_document_list.to_dict())
            _dict['documentList'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in signature_proof_list (list)
        _items = []
        if self.signature_proof_list:
            for _item_signature_proof_list in self.signature_proof_list:
                if _item_signature_proof_list:
                    _items.append(_item_signature_proof_list.to_dict())
            _dict['signatureProofList'] = _items
        # set to None if due_date (nullable) is None
        # and model_fields_set contains the field
        if self.due_date is None and "due_date" in self.model_fields_set:
            _dict['dueDate'] = None

        # set to None if origin_desk (nullable) is None
        # and model_fields_set contains the field
        if self.origin_desk is None and "origin_desk" in self.model_fields_set:
            _dict['originDesk'] = None

        # set to None if final_desk (nullable) is None
        # and model_fields_set contains the field
        if self.final_desk is None and "final_desk" in self.model_fields_set:
            _dict['finalDesk'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FolderDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "dueDate": obj.get("dueDate"),
            "metadata": obj.get("metadata"),
            "draftCreationDate": obj.get("draftCreationDate"),
            "type": TypeDto.from_dict(obj["type"]) if obj.get("type") is not None else None,
            "subtype": SubtypeDto.from_dict(obj["subtype"]) if obj.get("subtype") is not None else None,
            "originDesk": DeskRepresentation.from_dict(obj["originDesk"]) if obj.get("originDesk") is not None else None,
            "finalDesk": DeskRepresentation.from_dict(obj["finalDesk"]) if obj.get("finalDesk") is not None else None,
            "isReadByCurrentUser": obj.get("isReadByCurrentUser"),
            "legacyId": obj.get("legacyId"),
            "typeId": obj.get("typeId"),
            "subtypeId": obj.get("subtypeId"),
            "stepList": [Task.from_dict(_item) for _item in obj["stepList"]] if obj.get("stepList") is not None else None,
            "documentList": [DocumentDto.from_dict(_item) for _item in obj["documentList"]] if obj.get("documentList") is not None else None,
            "signatureProofList": [SignatureProof.from_dict(_item) for _item in obj["signatureProofList"]] if obj.get("signatureProofList") is not None else None,
            "readByUserIds": obj.get("readByUserIds"),
            "readByCurrentUser": obj.get("readByCurrentUser")
        })
        return _obj


