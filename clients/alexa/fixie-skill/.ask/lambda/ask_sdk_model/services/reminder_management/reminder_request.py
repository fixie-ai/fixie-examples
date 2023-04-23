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
    from ask_sdk_model.services.reminder_management.trigger import Trigger as Trigger_4ec8964
    from ask_sdk_model.services.reminder_management.push_notification import PushNotification as PushNotification_dd7adc41
    from ask_sdk_model.services.reminder_management.alert_info import AlertInfo as AlertInfo_97082f4b


class ReminderRequest(object):
    """
    Input request for creating a reminder


    :param request_time: Valid ISO 8601 format - Creation time of this reminder alert
    :type request_time: (optional) datetime
    :param trigger: 
    :type trigger: (optional) ask_sdk_model.services.reminder_management.trigger.Trigger
    :param alert_info: 
    :type alert_info: (optional) ask_sdk_model.services.reminder_management.alert_info.AlertInfo
    :param push_notification: 
    :type push_notification: (optional) ask_sdk_model.services.reminder_management.push_notification.PushNotification

    """
    deserialized_types = {
        'request_time': 'datetime',
        'trigger': 'ask_sdk_model.services.reminder_management.trigger.Trigger',
        'alert_info': 'ask_sdk_model.services.reminder_management.alert_info.AlertInfo',
        'push_notification': 'ask_sdk_model.services.reminder_management.push_notification.PushNotification'
    }  # type: Dict

    attribute_map = {
        'request_time': 'requestTime',
        'trigger': 'trigger',
        'alert_info': 'alertInfo',
        'push_notification': 'pushNotification'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, request_time=None, trigger=None, alert_info=None, push_notification=None):
        # type: (Optional[datetime], Optional[Trigger_4ec8964], Optional[AlertInfo_97082f4b], Optional[PushNotification_dd7adc41]) -> None
        """Input request for creating a reminder

        :param request_time: Valid ISO 8601 format - Creation time of this reminder alert
        :type request_time: (optional) datetime
        :param trigger: 
        :type trigger: (optional) ask_sdk_model.services.reminder_management.trigger.Trigger
        :param alert_info: 
        :type alert_info: (optional) ask_sdk_model.services.reminder_management.alert_info.AlertInfo
        :param push_notification: 
        :type push_notification: (optional) ask_sdk_model.services.reminder_management.push_notification.PushNotification
        """
        self.__discriminator_value = None  # type: str

        self.request_time = request_time
        self.trigger = trigger
        self.alert_info = alert_info
        self.push_notification = push_notification

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
        if not isinstance(other, ReminderRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
