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

from pydantic import BaseModel, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from miro_api.models.team_account_discovery_settings import TeamAccountDiscoverySettings
from miro_api.models.team_collaboration_settings import TeamCollaborationSettings
from miro_api.models.team_copy_access_level_settings import TeamCopyAccessLevelSettings
from miro_api.models.team_invitation_settings import TeamInvitationSettings
from miro_api.models.team_sharing_policy_settings import TeamSharingPolicySettings
from typing import Optional, Set
from typing_extensions import Self


class TeamSettings(BaseModel):
    """
    TeamSettings
    """  # noqa: E501

    organization_id: Optional[StrictStr] = Field(default=None, description="Organization id", alias="organizationId")
    team_account_discovery_settings: Optional[TeamAccountDiscoverySettings] = Field(
        default=None, alias="teamAccountDiscoverySettings"
    )
    team_collaboration_settings: Optional[TeamCollaborationSettings] = Field(
        default=None, alias="teamCollaborationSettings"
    )
    team_copy_access_level_settings: Optional[TeamCopyAccessLevelSettings] = Field(
        default=None, alias="teamCopyAccessLevelSettings"
    )
    team_id: Optional[StrictStr] = Field(default=None, description="Team id", alias="teamId")
    team_invitation_settings: Optional[TeamInvitationSettings] = Field(default=None, alias="teamInvitationSettings")
    team_sharing_policy_settings: Optional[TeamSharingPolicySettings] = Field(
        default=None, alias="teamSharingPolicySettings"
    )
    type: Optional[StrictStr] = Field(default="team-settings", description="Type of the object returned.")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = [
        "organizationId",
        "teamAccountDiscoverySettings",
        "teamCollaborationSettings",
        "teamCopyAccessLevelSettings",
        "teamId",
        "teamInvitationSettings",
        "teamSharingPolicySettings",
        "type",
    ]

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
        """Create an instance of TeamSettings from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of team_account_discovery_settings
        if self.team_account_discovery_settings:
            _dict["teamAccountDiscoverySettings"] = self.team_account_discovery_settings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of team_collaboration_settings
        if self.team_collaboration_settings:
            _dict["teamCollaborationSettings"] = self.team_collaboration_settings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of team_copy_access_level_settings
        if self.team_copy_access_level_settings:
            _dict["teamCopyAccessLevelSettings"] = self.team_copy_access_level_settings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of team_invitation_settings
        if self.team_invitation_settings:
            _dict["teamInvitationSettings"] = self.team_invitation_settings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of team_sharing_policy_settings
        if self.team_sharing_policy_settings:
            _dict["teamSharingPolicySettings"] = self.team_sharing_policy_settings.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TeamSettings from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "organizationId": obj.get("organizationId"),
                "teamAccountDiscoverySettings": (
                    TeamAccountDiscoverySettings.from_dict(obj["teamAccountDiscoverySettings"])
                    if obj.get("teamAccountDiscoverySettings") is not None
                    else None
                ),
                "teamCollaborationSettings": (
                    TeamCollaborationSettings.from_dict(obj["teamCollaborationSettings"])
                    if obj.get("teamCollaborationSettings") is not None
                    else None
                ),
                "teamCopyAccessLevelSettings": (
                    TeamCopyAccessLevelSettings.from_dict(obj["teamCopyAccessLevelSettings"])
                    if obj.get("teamCopyAccessLevelSettings") is not None
                    else None
                ),
                "teamId": obj.get("teamId"),
                "teamInvitationSettings": (
                    TeamInvitationSettings.from_dict(obj["teamInvitationSettings"])
                    if obj.get("teamInvitationSettings") is not None
                    else None
                ),
                "teamSharingPolicySettings": (
                    TeamSharingPolicySettings.from_dict(obj["teamSharingPolicySettings"])
                    if obj.get("teamSharingPolicySettings") is not None
                    else None
                ),
                "type": obj.get("type") if obj.get("type") is not None else "team-settings",
            }
        )
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
