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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from iparapheur_provisioning.models.desk_representation import DeskRepresentation
from iparapheur_provisioning.models.external_signature_config_representation import ExternalSignatureConfigRepresentation
from iparapheur_provisioning.models.seal_certificate_representation import SealCertificateRepresentation
from iparapheur_provisioning.models.subtype_layer_dto import SubtypeLayerDto
from iparapheur_provisioning.models.subtype_metadata_dto import SubtypeMetadataDto
from typing import Optional, Set
from typing_extensions import Self

class SubtypeDto(BaseModel):
    """
    SubtypeDto
    """ # noqa: E501
    id: Optional[StrictStr] = None
    name: Annotated[str, Field(min_length=2, strict=True, max_length=255)]
    description: Optional[Annotated[str, Field(min_length=3, strict=True, max_length=255)]] = None
    creation_workflow_id: Optional[StrictStr] = Field(default=None, alias="creationWorkflowId")
    validation_workflow_id: Optional[StrictStr] = Field(default=None, alias="validationWorkflowId")
    workflow_selection_script: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=65535)]] = Field(default=None, alias="workflowSelectionScript")
    annotations_allowed: Optional[StrictBool] = Field(default=None, alias="annotationsAllowed")
    external_signature_automatic: Optional[StrictBool] = Field(default=None, alias="externalSignatureAutomatic")
    secure_mail_server_id: Optional[StrictInt] = Field(default=None, alias="secureMailServerId")
    seal_certificate_id: Optional[StrictStr] = Field(default=None, alias="sealCertificateId")
    seal_certificate: Optional[SealCertificateRepresentation] = Field(default=None, alias="sealCertificate")
    subtype_metadata_list: Optional[List[SubtypeMetadataDto]] = Field(default=None, alias="subtypeMetadataList")
    subtype_layers: Optional[List[SubtypeLayerDto]] = Field(default=None, alias="subtypeLayers")
    external_signature_config_id: Optional[StrictStr] = Field(default=None, alias="externalSignatureConfigId")
    external_signature_config: Optional[ExternalSignatureConfigRepresentation] = Field(default=None, alias="externalSignatureConfig")
    creation_permitted_desk_ids: Optional[List[Optional[StrictStr]]] = Field(default=None, alias="creationPermittedDeskIds")
    creation_permitted_desks: Optional[List[Optional[DeskRepresentation]]] = Field(default=None, alias="creationPermittedDesks")
    filterable_by_desk_ids: Optional[List[Optional[StrictStr]]] = Field(default=None, alias="filterableByDeskIds")
    filterable_by_desks: Optional[List[Optional[DeskRepresentation]]] = Field(default=None, alias="filterableByDesks")
    max_main_documents: Optional[StrictInt] = Field(default=None, alias="maxMainDocuments")
    multi_documents: Optional[StrictBool] = Field(default=None, alias="multiDocuments")
    digital_signature_mandatory: Optional[StrictBool] = Field(default=None, alias="digitalSignatureMandatory")
    reading_mandatory: Optional[StrictBool] = Field(default=None, alias="readingMandatory")
    annexe_included: Optional[StrictBool] = Field(default=None, alias="annexeIncluded")
    seal_automatic: Optional[StrictBool] = Field(default=None, alias="sealAutomatic")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "creationWorkflowId", "validationWorkflowId", "workflowSelectionScript", "annotationsAllowed", "externalSignatureAutomatic", "secureMailServerId", "sealCertificateId", "sealCertificate", "subtypeMetadataList", "subtypeLayers", "externalSignatureConfigId", "externalSignatureConfig", "creationPermittedDeskIds", "creationPermittedDesks", "filterableByDeskIds", "filterableByDesks", "maxMainDocuments", "multiDocuments", "digitalSignatureMandatory", "readingMandatory", "annexeIncluded", "sealAutomatic"]

    @field_validator('name')
    def name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[^\r\n ]*$", value):
            raise ValueError(r"must validate the regular expression /^[^\r\n ]*$/")
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
        """Create an instance of SubtypeDto from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "id",
            "creation_permitted_desks",
            "filterable_by_desks",
            "max_main_documents",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of seal_certificate
        if self.seal_certificate:
            _dict['sealCertificate'] = self.seal_certificate.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in subtype_metadata_list (list)
        _items = []
        if self.subtype_metadata_list:
            for _item_subtype_metadata_list in self.subtype_metadata_list:
                if _item_subtype_metadata_list:
                    _items.append(_item_subtype_metadata_list.to_dict())
            _dict['subtypeMetadataList'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in subtype_layers (list)
        _items = []
        if self.subtype_layers:
            for _item_subtype_layers in self.subtype_layers:
                if _item_subtype_layers:
                    _items.append(_item_subtype_layers.to_dict())
            _dict['subtypeLayers'] = _items
        # override the default output from pydantic by calling `to_dict()` of external_signature_config
        if self.external_signature_config:
            _dict['externalSignatureConfig'] = self.external_signature_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in creation_permitted_desks (list)
        _items = []
        if self.creation_permitted_desks:
            for _item_creation_permitted_desks in self.creation_permitted_desks:
                if _item_creation_permitted_desks:
                    _items.append(_item_creation_permitted_desks.to_dict())
            _dict['creationPermittedDesks'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in filterable_by_desks (list)
        _items = []
        if self.filterable_by_desks:
            for _item_filterable_by_desks in self.filterable_by_desks:
                if _item_filterable_by_desks:
                    _items.append(_item_filterable_by_desks.to_dict())
            _dict['filterableByDesks'] = _items
        # set to None if creation_workflow_id (nullable) is None
        # and model_fields_set contains the field
        if self.creation_workflow_id is None and "creation_workflow_id" in self.model_fields_set:
            _dict['creationWorkflowId'] = None

        # set to None if workflow_selection_script (nullable) is None
        # and model_fields_set contains the field
        if self.workflow_selection_script is None and "workflow_selection_script" in self.model_fields_set:
            _dict['workflowSelectionScript'] = None

        # set to None if secure_mail_server_id (nullable) is None
        # and model_fields_set contains the field
        if self.secure_mail_server_id is None and "secure_mail_server_id" in self.model_fields_set:
            _dict['secureMailServerId'] = None

        # set to None if seal_certificate_id (nullable) is None
        # and model_fields_set contains the field
        if self.seal_certificate_id is None and "seal_certificate_id" in self.model_fields_set:
            _dict['sealCertificateId'] = None

        # set to None if seal_certificate (nullable) is None
        # and model_fields_set contains the field
        if self.seal_certificate is None and "seal_certificate" in self.model_fields_set:
            _dict['sealCertificate'] = None

        # set to None if external_signature_config_id (nullable) is None
        # and model_fields_set contains the field
        if self.external_signature_config_id is None and "external_signature_config_id" in self.model_fields_set:
            _dict['externalSignatureConfigId'] = None

        # set to None if external_signature_config (nullable) is None
        # and model_fields_set contains the field
        if self.external_signature_config is None and "external_signature_config" in self.model_fields_set:
            _dict['externalSignatureConfig'] = None

        # set to None if creation_permitted_desk_ids (nullable) is None
        # and model_fields_set contains the field
        if self.creation_permitted_desk_ids is None and "creation_permitted_desk_ids" in self.model_fields_set:
            _dict['creationPermittedDeskIds'] = None

        # set to None if creation_permitted_desks (nullable) is None
        # and model_fields_set contains the field
        if self.creation_permitted_desks is None and "creation_permitted_desks" in self.model_fields_set:
            _dict['creationPermittedDesks'] = None

        # set to None if filterable_by_desk_ids (nullable) is None
        # and model_fields_set contains the field
        if self.filterable_by_desk_ids is None and "filterable_by_desk_ids" in self.model_fields_set:
            _dict['filterableByDeskIds'] = None

        # set to None if filterable_by_desks (nullable) is None
        # and model_fields_set contains the field
        if self.filterable_by_desks is None and "filterable_by_desks" in self.model_fields_set:
            _dict['filterableByDesks'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SubtypeDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "creationWorkflowId": obj.get("creationWorkflowId"),
            "validationWorkflowId": obj.get("validationWorkflowId"),
            "workflowSelectionScript": obj.get("workflowSelectionScript"),
            "annotationsAllowed": obj.get("annotationsAllowed"),
            "externalSignatureAutomatic": obj.get("externalSignatureAutomatic"),
            "secureMailServerId": obj.get("secureMailServerId"),
            "sealCertificateId": obj.get("sealCertificateId"),
            "sealCertificate": SealCertificateRepresentation.from_dict(obj["sealCertificate"]) if obj.get("sealCertificate") is not None else None,
            "subtypeMetadataList": [SubtypeMetadataDto.from_dict(_item) for _item in obj["subtypeMetadataList"]] if obj.get("subtypeMetadataList") is not None else None,
            "subtypeLayers": [SubtypeLayerDto.from_dict(_item) for _item in obj["subtypeLayers"]] if obj.get("subtypeLayers") is not None else None,
            "externalSignatureConfigId": obj.get("externalSignatureConfigId"),
            "externalSignatureConfig": ExternalSignatureConfigRepresentation.from_dict(obj["externalSignatureConfig"]) if obj.get("externalSignatureConfig") is not None else None,
            "creationPermittedDeskIds": obj.get("creationPermittedDeskIds"),
            "creationPermittedDesks": [DeskRepresentation.from_dict(_item) for _item in obj["creationPermittedDesks"]] if obj.get("creationPermittedDesks") is not None else None,
            "filterableByDeskIds": obj.get("filterableByDeskIds"),
            "filterableByDesks": [DeskRepresentation.from_dict(_item) for _item in obj["filterableByDesks"]] if obj.get("filterableByDesks") is not None else None,
            "maxMainDocuments": obj.get("maxMainDocuments"),
            "multiDocuments": obj.get("multiDocuments"),
            "digitalSignatureMandatory": obj.get("digitalSignatureMandatory"),
            "readingMandatory": obj.get("readingMandatory"),
            "annexeIncluded": obj.get("annexeIncluded"),
            "sealAutomatic": obj.get("sealAutomatic")
        })
        return _obj


