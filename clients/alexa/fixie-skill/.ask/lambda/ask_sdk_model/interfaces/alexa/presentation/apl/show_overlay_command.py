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
from ask_sdk_model.interfaces.alexa.presentation.apl.command import Command


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime


class ShowOverlayCommand(Command):
    """
    ShowOverlay Command used by television shopping skill.


    :param delay: The delay in milliseconds before this command starts executing; must be non-negative. Defaults to 0.
    :type delay: (optional) int
    :param description: A user-provided description of this command.
    :type description: (optional) str
    :param screen_lock: If true, disable the Interaction Timer.
    :type screen_lock: (optional) bool
    :param sequencer: Specify the sequencer that should execute this command.
    :type sequencer: (optional) str
    :param when: If false, the execution of the command is skipped. Defaults to true.
    :type when: (optional) bool
    :param overlay_layout_id: The id of overlay Layout.
    :type overlay_layout_id: (optional) str
    :param underlying_layout_id: The id of underlying Layout.
    :type underlying_layout_id: (optional) str
    :param overlay_width: The overlay width.
    :type overlay_width: (optional) str
    :param duration: The duration of ShowOverlay Command.
    :type duration: (optional) int

    """
    deserialized_types = {
        'object_type': 'str',
        'delay': 'int',
        'description': 'str',
        'screen_lock': 'bool',
        'sequencer': 'str',
        'when': 'bool',
        'overlay_layout_id': 'str',
        'underlying_layout_id': 'str',
        'overlay_width': 'str',
        'duration': 'int'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'delay': 'delay',
        'description': 'description',
        'screen_lock': 'screenLock',
        'sequencer': 'sequencer',
        'when': 'when',
        'overlay_layout_id': 'overlayLayoutId',
        'underlying_layout_id': 'underlyingLayoutId',
        'overlay_width': 'overlayWidth',
        'duration': 'duration'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, delay=None, description=None, screen_lock=None, sequencer=None, when=None, overlay_layout_id=None, underlying_layout_id=None, overlay_width=None, duration=None):
        # type: (Union[int, str, None], Optional[str], Optional[bool], Optional[str], Optional[bool], Optional[str], Optional[str], Optional[str], Optional[int]) -> None
        """ShowOverlay Command used by television shopping skill.

        :param delay: The delay in milliseconds before this command starts executing; must be non-negative. Defaults to 0.
        :type delay: (optional) int
        :param description: A user-provided description of this command.
        :type description: (optional) str
        :param screen_lock: If true, disable the Interaction Timer.
        :type screen_lock: (optional) bool
        :param sequencer: Specify the sequencer that should execute this command.
        :type sequencer: (optional) str
        :param when: If false, the execution of the command is skipped. Defaults to true.
        :type when: (optional) bool
        :param overlay_layout_id: The id of overlay Layout.
        :type overlay_layout_id: (optional) str
        :param underlying_layout_id: The id of underlying Layout.
        :type underlying_layout_id: (optional) str
        :param overlay_width: The overlay width.
        :type overlay_width: (optional) str
        :param duration: The duration of ShowOverlay Command.
        :type duration: (optional) int
        """
        self.__discriminator_value = "ShowOverlay"  # type: str

        self.object_type = self.__discriminator_value
        super(ShowOverlayCommand, self).__init__(object_type=self.__discriminator_value, delay=delay, description=description, screen_lock=screen_lock, sequencer=sequencer, when=when)
        self.overlay_layout_id = overlay_layout_id
        self.underlying_layout_id = underlying_layout_id
        self.overlay_width = overlay_width
        self.duration = duration

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
        if not isinstance(other, ShowOverlayCommand):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
