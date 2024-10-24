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

from pydantic import BaseModel, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self


class EmbedDataResponse(BaseModel):
    """
    EmbedDataResponse
    """  # noqa: E501

    content_type: Optional[StrictStr] = Field(
        default=None, description="Type of the embedded item's content.", alias="contentType"
    )
    description: Optional[StrictStr] = Field(default=None, description="Short description of the embedded item.")
    html: Optional[StrictStr] = Field(default=None, description="HTML code of the embedded item.")
    mode: Optional[StrictStr] = Field(
        default=None,
        description="Defines how the content in the embed item is displayed on the board. `inline`: The embedded content is displayed directly on the board. `modal`: The embedded content is displayed inside a modal overlay on the board.",
    )
    preview_url: Optional[StrictStr] = Field(
        default=None,
        description="The URL to download the resource. You must use your access token to access the URL. The URL contains the `redirect` parameter and the `format` parameter to control the request execution as described in the following parameters: `format` parameter: By default, the image format is set to the preview image. If you want to download the original image, set the `format` parameter in the URL to `original`. `redirect`: By default, the `redirect` parameter is set to `false` and the resource object containing the URL and the resource type is returned with a 200 OK HTTP code. This URL is valid for 60 seconds. You can use this URL to retrieve the resource file. If the `redirect` parameter is set to `true`, a 307 TEMPORARY_REDIRECT HTTP response is returned. If you follow HTTP 3xx responses as redirects, you will automatically be redirected to the resource file and the content type returned can be `image/png`, 'image/svg', or 'image/jpg', depending on the original image type.",
        alias="previewUrl",
    )
    provider_name: Optional[StrictStr] = Field(
        default=None, description="Name of the content's provider.", alias="providerName"
    )
    provider_url: Optional[StrictStr] = Field(
        default=None, description="Url of the content's provider.", alias="providerUrl"
    )
    title: Optional[StrictStr] = Field(default=None, description="Title of the embedded item.")
    url: Optional[StrictStr] = Field(
        default=None,
        description="A [valid URL](https://developers.miro.com/reference/data#embeddata) pointing to the content resource that you want to embed in the board. Possible transport protocols: HTTP, HTTPS.",
    )
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = [
        "contentType",
        "description",
        "html",
        "mode",
        "previewUrl",
        "providerName",
        "providerUrl",
        "title",
        "url",
    ]

    @field_validator("mode")
    def mode_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["inline", "modal"]):
            raise ValueError("must be one of enum values ('inline', 'modal')")
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
        """Create an instance of EmbedDataResponse from a JSON string"""
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
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of EmbedDataResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "contentType": obj.get("contentType"),
                "description": obj.get("description"),
                "html": obj.get("html"),
                "mode": obj.get("mode"),
                "previewUrl": obj.get("previewUrl"),
                "providerName": obj.get("providerName"),
                "providerUrl": obj.get("providerUrl"),
                "title": obj.get("title"),
                "url": obj.get("url"),
            }
        )
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
