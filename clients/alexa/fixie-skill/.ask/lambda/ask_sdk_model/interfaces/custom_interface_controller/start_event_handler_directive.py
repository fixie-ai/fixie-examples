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
from ask_sdk_model.directive import Directive


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.interfaces.custom_interface_controller.event_filter import EventFilter as EventFilter_321cde63
    from ask_sdk_model.interfaces.custom_interface_controller.expiration import Expiration as Expiration_edfb772c


class StartEventHandlerDirective(Directive):
    """
    This directive configures and starts an event handler. This will enable the skill to receive Custom Events. A skill can only have one active Event Handler at a time.


    :param token: A unique string to identify the Event Handler. This identifier is associated with all events dispatched by the Event Handler while it is active.
    :type token: (optional) str
    :param event_filter: 
    :type event_filter: (optional) ask_sdk_model.interfaces.custom_interface_controller.event_filter.EventFilter
    :param expiration: 
    :type expiration: (optional) ask_sdk_model.interfaces.custom_interface_controller.expiration.Expiration

    """
    deserialized_types = {
        'object_type': 'str',
        'token': 'str',
        'event_filter': 'ask_sdk_model.interfaces.custom_interface_controller.event_filter.EventFilter',
        'expiration': 'ask_sdk_model.interfaces.custom_interface_controller.expiration.Expiration'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'token': 'token',
        'event_filter': 'eventFilter',
        'expiration': 'expiration'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, token=None, event_filter=None, expiration=None):
        # type: (Optional[str], Optional[EventFilter_321cde63], Optional[Expiration_edfb772c]) -> None
        """This directive configures and starts an event handler. This will enable the skill to receive Custom Events. A skill can only have one active Event Handler at a time.

        :param token: A unique string to identify the Event Handler. This identifier is associated with all events dispatched by the Event Handler while it is active.
        :type token: (optional) str
        :param event_filter: 
        :type event_filter: (optional) ask_sdk_model.interfaces.custom_interface_controller.event_filter.EventFilter
        :param expiration: 
        :type expiration: (optional) ask_sdk_model.interfaces.custom_interface_controller.expiration.Expiration
        """
        self.__discriminator_value = "CustomInterfaceController.StartEventHandler"  # type: str

        self.object_type = self.__discriminator_value
        super(StartEventHandlerDirective, self).__init__(object_type=self.__discriminator_value)
        self.token = token
        self.event_filter = event_filter
        self.expiration = expiration

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
        if not isinstance(other, StartEventHandlerDirective):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
