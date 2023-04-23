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
from abc import ABCMeta, abstractmethod


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime


class Command(object):
    """
    A message that can change the visual or audio presentation of the content on the screen.


    :param object_type: Defines the command type and dictates which properties must/can be included.
    :type object_type: (optional) str
    :param delay: The delay in milliseconds before this command starts executing; must be non-negative. Defaults to 0.
    :type delay: (optional) int
    :param description: A user-provided description of this command.
    :type description: (optional) str
    :param screen_lock: If true, disable the Interaction Timer.
    :type screen_lock: (optional) bool
    :param when: A conditional expression to be evaluated in device. If false, the execution of the command is skipped. Defaults to true.
    :type when: (optional) bool

    .. note::

        This is an abstract class. Use the following mapping, to figure out
        the model class to be instantiated, that sets ``type`` variable.

        | SetValue: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.set_value_command.SetValueCommand`,
        |
        | Idle: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.idle_command.IdleCommand`,
        |
        | AutoPage: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.auto_page_command.AutoPageCommand`,
        |
        | Scroll: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.scroll_command.ScrollCommand`,
        |
        | SendEvent: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.send_event_command.SendEventCommand`,
        |
        | Parallel: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.parallel_command.ParallelCommand`,
        |
        | SetPage: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.set_page_command.SetPageCommand`,
        |
        | Sequential: :py:class:`ask_sdk_model.interfaces.alexa.presentation.aplt.sequential_command.SequentialCommand`

    """
    deserialized_types = {
        'object_type': 'str',
        'delay': 'int',
        'description': 'str',
        'screen_lock': 'bool',
        'when': 'bool'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'delay': 'delay',
        'description': 'description',
        'screen_lock': 'screenLock',
        'when': 'when'
    }  # type: Dict
    supports_multiple_types = False

    discriminator_value_class_map = {
        'SetValue': 'ask_sdk_model.interfaces.alexa.presentation.aplt.set_value_command.SetValueCommand',
        'Idle': 'ask_sdk_model.interfaces.alexa.presentation.aplt.idle_command.IdleCommand',
        'AutoPage': 'ask_sdk_model.interfaces.alexa.presentation.aplt.auto_page_command.AutoPageCommand',
        'Scroll': 'ask_sdk_model.interfaces.alexa.presentation.aplt.scroll_command.ScrollCommand',
        'SendEvent': 'ask_sdk_model.interfaces.alexa.presentation.aplt.send_event_command.SendEventCommand',
        'Parallel': 'ask_sdk_model.interfaces.alexa.presentation.aplt.parallel_command.ParallelCommand',
        'SetPage': 'ask_sdk_model.interfaces.alexa.presentation.aplt.set_page_command.SetPageCommand',
        'Sequential': 'ask_sdk_model.interfaces.alexa.presentation.aplt.sequential_command.SequentialCommand'
    }

    json_discriminator_key = "type"

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, object_type=None, delay=None, description=None, screen_lock=None, when=None):
        # type: (Optional[str], Optional[int], Optional[str], Optional[bool], Union[bool, str, None]) -> None
        """A message that can change the visual or audio presentation of the content on the screen.

        :param object_type: Defines the command type and dictates which properties must/can be included.
        :type object_type: (optional) str
        :param delay: The delay in milliseconds before this command starts executing; must be non-negative. Defaults to 0.
        :type delay: (optional) int
        :param description: A user-provided description of this command.
        :type description: (optional) str
        :param screen_lock: If true, disable the Interaction Timer.
        :type screen_lock: (optional) bool
        :param when: A conditional expression to be evaluated in device. If false, the execution of the command is skipped. Defaults to true.
        :type when: (optional) bool
        """
        self.__discriminator_value = None  # type: str

        self.object_type = object_type
        self.delay = delay
        self.description = description
        self.screen_lock = screen_lock
        self.when = when

    @classmethod
    def get_real_child_model(cls, data):
        # type: (Dict[str, str]) -> Optional[str]
        """Returns the real base class specified by the discriminator"""
        discriminator_value = data[cls.json_discriminator_key]
        return cls.discriminator_value_class_map.get(discriminator_value)

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
        if not isinstance(other, Command):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
