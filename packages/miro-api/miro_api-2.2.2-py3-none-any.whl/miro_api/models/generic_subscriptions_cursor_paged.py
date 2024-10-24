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

from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from miro_api.models.generic_subscription import GenericSubscription
from typing import Optional, Set
from typing_extensions import Self


class GenericSubscriptionsCursorPaged(BaseModel):
    """
    GenericSubscriptionsCursorPaged
    """  # noqa: E501

    cursor: Optional[StrictStr] = Field(
        default=None,
        description="A cursor-paginated method returns a portion of the total set of results based on the `limit` specified and a `cursor` that points to the next portion of the results. To retrieve the next set of results of the collection, set the `cursor` parameter in your next request to the value returned in this parameter.",
    )
    data: Optional[List[GenericSubscription]] = Field(default=None, description="Contains the result data.")
    limit: Optional[StrictInt] = Field(
        default=None,
        description="Maximum number of results returned based on the `limit` specified in the request. For example, if there are `20` results, the request has no `cursor` value, and the `limit` is set to `20`,the `size` of the results will be `20`. The rest of the results will not be returned. To retrieve the rest of the results, you must make another request and set the appropriate value for the `cursor` parameter value that you obtained from the response.",
    )
    size: Optional[StrictInt] = Field(
        default=None,
        description="Number of results returned in the response considering the `cursor` and the `limit` values sent in the request. For example, if there are `20` results, the request does not have a `cursor` value, and the `limit` set to `10`, the `size` of the results will be `10`.<br>In this example, the response will also return a cursor value that can be used to retrieve the next set of 10 remaining results in the collection.",
    )
    total: Optional[StrictInt] = Field(
        default=None,
        description="Total number of results available. If the value of the `total` parameter is higher than the value of the `size` parameter, this means that there are more results that you can retrieve. To retrieve more results, you can make another request and set the `offset` value accordingly. For example, if there are `30` results, and the request has the `offset` set to `0` and the `limit` set to `20`, the `size` parameter will return `20` and the `total` parameter will return `30`. This means that there are 9 more results to retrieve (as the offset is zero-based).",
    )
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["cursor", "data", "limit", "size", "total"]

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
        """Create an instance of GenericSubscriptionsCursorPaged from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in data (list)
        _items = []
        if self.data:
            for _item in self.data:
                if _item:
                    _items.append(_item.to_dict())
            _dict["data"] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GenericSubscriptionsCursorPaged from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "cursor": obj.get("cursor"),
                "data": (
                    [GenericSubscription.from_dict(_item) for _item in obj["data"]]
                    if obj.get("data") is not None
                    else None
                ),
                "limit": obj.get("limit"),
                "size": obj.get("size"),
                "total": obj.get("total"),
            }
        )
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
