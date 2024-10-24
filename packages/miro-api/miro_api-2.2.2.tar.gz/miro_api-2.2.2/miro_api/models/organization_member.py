# coding: utf-8

"""
    Miro Developer Platform

    <img src=\"https://content.pstmn.io/47449ea6-0ef7-4af2-bac1-e58a70e61c58/aW1hZ2UucG5n\" width=\"1685\" height=\"593\">  ### Miro Developer Platform concepts  - New to the Miro Developer Platform? Interested in learning more about platform concepts?? [Read our introduction page](https://beta.developers.miro.com/docs/introduction) and familiarize yourself with the Miro Developer Platform capabilities in a few minutes.   ### Getting started with the Miro REST API  - [Quickstart (video):](https://beta.developers.miro.com/docs/try-out-the-rest-api-in-less-than-3-minutes) try the REST API in less than 3 minutes. - [Quickstart (article):](https://beta.developers.miro.com/docs/build-your-first-hello-world-app-1) get started and try the REST API in less than 3 minutes.   ### Miro REST API tutorials  Check out our how-to articles with step-by-step instructions and code examples so you can:  - [Get started with OAuth 2.0 and Miro](https://beta.developers.miro.com/docs/getting-started-with-oauth)   ### Miro App Examples  Clone our [Miro App Examples repository](https://github.com/miroapp/app-examples) to get inspiration, customize, and explore apps built on top of Miro's Developer Platform 2.0. 

    The version of the OpenAPI document: v2.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from miro_api.models.admin_role import AdminRole
from typing import Optional, Set
from typing_extensions import Self


class OrganizationMember(BaseModel):
    """
    Organization member
    """  # noqa: E501

    id: StrictStr = Field(description="Id of the user")
    active: StrictBool = Field(
        description='Indicates if a user is active or deactivated. Learn more about <a target="blank" href="https://help.miro.com/hc/en-us/articles/360025025894-Deactivated-users">user deactivation</a>.'
    )
    email: StrictStr = Field(description="User email")
    last_activity_at: Optional[datetime] = Field(
        default=None,
        description="Date and time when the user was last active. <br>Format: UTC, adheres to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601), includes a [trailing Z offset](https://en.wikipedia.org/wiki/ISO_8601#Coordinated_Universal_Time_(UTC)). If the user never logged in, the parameter value is empty. ",
        alias="lastActivityAt",
    )
    license: StrictStr = Field(description="Name of the current user license in the organization")
    license_assigned_at: Optional[datetime] = Field(
        default=None, description="Time when the license was assigned to the user", alias="licenseAssignedAt"
    )
    role: StrictStr = Field(description="Name of the user role in the organization")
    type: Optional[StrictStr] = Field(default="organization-member", description="Type of the object returned.")
    admin_roles: Optional[List[AdminRole]] = Field(
        default=None, description="List of admin roles assigned to the user", alias="adminRoles"
    )
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = [
        "id",
        "active",
        "email",
        "lastActivityAt",
        "license",
        "licenseAssignedAt",
        "role",
        "type",
        "adminRoles",
    ]

    @field_validator("license")
    def license_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(["full", "occasional", "free", "free_restricted", "full_trial", "unknown"]):
            raise ValueError(
                "must be one of enum values ('full', 'occasional', 'free', 'free_restricted', 'full_trial', 'unknown')"
            )
        return value

    @field_validator("role")
    def role_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(
            [
                "organization_internal_admin",
                "organization_internal_user",
                "organization_external_user",
                "organization_team_guest_user",
                "unknown",
            ]
        ):
            raise ValueError(
                "must be one of enum values ('organization_internal_admin', 'organization_internal_user', 'organization_external_user', 'organization_team_guest_user', 'unknown')"
            )
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of OrganizationMember from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * Fields in `self.additional_properties` are added to the output dict.
        """
        excluded_fields: Set[str] = set(
            [
                "additional_properties",
            ]
        )

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in admin_roles (list)
        _items = []
        if self.admin_roles:
            for _item in self.admin_roles:
                if _item:
                    _items.append(_item.to_dict())
            _dict["adminRoles"] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OrganizationMember from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "active": obj.get("active"),
                "email": obj.get("email"),
                "lastActivityAt": obj.get("lastActivityAt"),
                "license": obj.get("license"),
                "licenseAssignedAt": obj.get("licenseAssignedAt"),
                "role": obj.get("role"),
                "type": obj.get("type") if obj.get("type") is not None else "organization-member",
                "adminRoles": (
                    [AdminRole.from_dict(_item) for _item in obj["adminRoles"]]
                    if obj.get("adminRoles") is not None
                    else None
                ),
            }
        )
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
