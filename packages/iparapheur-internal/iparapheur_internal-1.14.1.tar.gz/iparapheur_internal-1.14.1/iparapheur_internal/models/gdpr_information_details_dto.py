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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from iparapheur_internal.models.gdpr_application import GdprApplication
from iparapheur_internal.models.gdpr_declaring_entity import GdprDeclaringEntity
from iparapheur_internal.models.gdpr_entity import GdprEntity
from typing import Optional, Set
from typing_extensions import Self

class GdprInformationDetailsDto(BaseModel):
    """
    GdprInformationDetailsDto
    """ # noqa: E501
    declaring_entity: Optional[GdprDeclaringEntity] = Field(default=None, alias="declaringEntity")
    hosting_entity_comments: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=255)]] = Field(default=None, alias="hostingEntityComments")
    hosting_entity: Optional[GdprEntity] = Field(default=None, alias="hostingEntity")
    maintenance_entity: Optional[GdprEntity] = Field(default=None, alias="maintenanceEntity")
    application: Optional[GdprApplication] = None
    __properties: ClassVar[List[str]] = ["declaringEntity", "hostingEntityComments", "hostingEntity", "maintenanceEntity", "application"]

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
        """Create an instance of GdprInformationDetailsDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of declaring_entity
        if self.declaring_entity:
            _dict['declaringEntity'] = self.declaring_entity.to_dict()
        # override the default output from pydantic by calling `to_dict()` of hosting_entity
        if self.hosting_entity:
            _dict['hostingEntity'] = self.hosting_entity.to_dict()
        # override the default output from pydantic by calling `to_dict()` of maintenance_entity
        if self.maintenance_entity:
            _dict['maintenanceEntity'] = self.maintenance_entity.to_dict()
        # override the default output from pydantic by calling `to_dict()` of application
        if self.application:
            _dict['application'] = self.application.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GdprInformationDetailsDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "declaringEntity": GdprDeclaringEntity.from_dict(obj["declaringEntity"]) if obj.get("declaringEntity") is not None else None,
            "hostingEntityComments": obj.get("hostingEntityComments"),
            "hostingEntity": GdprEntity.from_dict(obj["hostingEntity"]) if obj.get("hostingEntity") is not None else None,
            "maintenanceEntity": GdprEntity.from_dict(obj["maintenanceEntity"]) if obj.get("maintenanceEntity") is not None else None,
            "application": GdprApplication.from_dict(obj["application"]) if obj.get("application") is not None else None
        })
        return _obj


