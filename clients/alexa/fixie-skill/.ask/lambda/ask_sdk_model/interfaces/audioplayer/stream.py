# coding: utf-8

#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#

import pprint
import re  # noqa: F401
import six
import typing
from enum import Enum


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.interfaces.audioplayer.caption_data import CaptionData as CaptionData_e119f120


class Stream(object):
    """

    :param expected_previous_token: 
    :type expected_previous_token: (optional) str
    :param token: 
    :type token: (optional) str
    :param url: 
    :type url: (optional) str
    :param offset_in_milliseconds: 
    :type offset_in_milliseconds: (optional) int
    :param caption_data: 
    :type caption_data: (optional) ask_sdk_model.interfaces.audioplayer.caption_data.CaptionData

    """
    deserialized_types = {
        'expected_previous_token': 'str',
        'token': 'str',
        'url': 'str',
        'offset_in_milliseconds': 'int',
        'caption_data': 'ask_sdk_model.interfaces.audioplayer.caption_data.CaptionData'
    }  # type: Dict

    attribute_map = {
        'expected_previous_token': 'expectedPreviousToken',
        'token': 'token',
        'url': 'url',
        'offset_in_milliseconds': 'offsetInMilliseconds',
        'caption_data': 'captionData'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, expected_previous_token=None, token=None, url=None, offset_in_milliseconds=None, caption_data=None):
        # type: (Optional[str], Optional[str], Optional[str], Optional[int], Optional[CaptionData_e119f120]) -> None
        """

        :param expected_previous_token: 
        :type expected_previous_token: (optional) str
        :param token: 
        :type token: (optional) str
        :param url: 
        :type url: (optional) str
        :param offset_in_milliseconds: 
        :type offset_in_milliseconds: (optional) int
        :param caption_data: 
        :type caption_data: (optional) ask_sdk_model.interfaces.audioplayer.caption_data.CaptionData
        """
        self.__discriminator_value = None  # type: str

        self.expected_previous_token = expected_previous_token
        self.token = token
        self.url = url
        self.offset_in_milliseconds = offset_in_milliseconds
        self.caption_data = caption_data

    def to_dict(self):
        # type: () -> Dict[str, object]
        """Returns the model properties as a dict"""
        result = {}  # type: Dict

        for attr, _ in six.iteritems(self.deserialized_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else
                    x.value if isinstance(x, Enum) else x,
                    value
                ))
            elif isinstance(value, Enum):
                result[attr] = value.value
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else
                    (item[0], item[1].value)
                    if isinstance(item[1], Enum) else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        # type: () -> str
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        # type: () -> str
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are equal"""
        if not isinstance(other, Stream):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
