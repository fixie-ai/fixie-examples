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
    from ask_sdk_model.services.reminder_management.status import Status as Status_fbbd2410


class ReminderResponse(object):
    """
    Response object for post/put/delete reminder request


    :param alert_token: Unique id of this reminder alert
    :type alert_token: (optional) str
    :param created_time: Valid ISO 8601 format - Creation time of this reminder alert
    :type created_time: (optional) str
    :param updated_time: Valid ISO 8601 format - Last updated time of this reminder alert
    :type updated_time: (optional) str
    :param status: 
    :type status: (optional) ask_sdk_model.services.reminder_management.status.Status
    :param version: Version of reminder alert
    :type version: (optional) str
    :param href: URI to retrieve the created alert
    :type href: (optional) str

    """
    deserialized_types = {
        'alert_token': 'str',
        'created_time': 'str',
        'updated_time': 'str',
        'status': 'ask_sdk_model.services.reminder_management.status.Status',
        'version': 'str',
        'href': 'str'
    }  # type: Dict

    attribute_map = {
        'alert_token': 'alertToken',
        'created_time': 'createdTime',
        'updated_time': 'updatedTime',
        'status': 'status',
        'version': 'version',
        'href': 'href'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, alert_token=None, created_time=None, updated_time=None, status=None, version=None, href=None):
        # type: (Optional[str], Optional[str], Optional[str], Optional[Status_fbbd2410], Optional[str], Optional[str]) -> None
        """Response object for post/put/delete reminder request

        :param alert_token: Unique id of this reminder alert
        :type alert_token: (optional) str
        :param created_time: Valid ISO 8601 format - Creation time of this reminder alert
        :type created_time: (optional) str
        :param updated_time: Valid ISO 8601 format - Last updated time of this reminder alert
        :type updated_time: (optional) str
        :param status: 
        :type status: (optional) ask_sdk_model.services.reminder_management.status.Status
        :param version: Version of reminder alert
        :type version: (optional) str
        :param href: URI to retrieve the created alert
        :type href: (optional) str
        """
        self.__discriminator_value = None  # type: str

        self.alert_token = alert_token
        self.created_time = created_time
        self.updated_time = updated_time
        self.status = status
        self.version = version
        self.href = href

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
        if not isinstance(other, ReminderResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
