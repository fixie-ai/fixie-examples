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
from ask_sdk_model.interfaces.display.template import Template


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.interfaces.display.image import Image as Image_1942d978
    from ask_sdk_model.interfaces.display.text_content import TextContent as TextContent_1d3959d5
    from ask_sdk_model.interfaces.display.back_button_behavior import BackButtonBehavior as BackButtonBehavior_46c3eb02


class BodyTemplate1(Template):
    """

    :param token: 
    :type token: (optional) str
    :param back_button: 
    :type back_button: (optional) ask_sdk_model.interfaces.display.back_button_behavior.BackButtonBehavior
    :param background_image: 
    :type background_image: (optional) ask_sdk_model.interfaces.display.image.Image
    :param title: 
    :type title: (optional) str
    :param text_content: 
    :type text_content: (optional) ask_sdk_model.interfaces.display.text_content.TextContent

    """
    deserialized_types = {
        'object_type': 'str',
        'token': 'str',
        'back_button': 'ask_sdk_model.interfaces.display.back_button_behavior.BackButtonBehavior',
        'background_image': 'ask_sdk_model.interfaces.display.image.Image',
        'title': 'str',
        'text_content': 'ask_sdk_model.interfaces.display.text_content.TextContent'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'token': 'token',
        'back_button': 'backButton',
        'background_image': 'backgroundImage',
        'title': 'title',
        'text_content': 'textContent'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, token=None, back_button=None, background_image=None, title=None, text_content=None):
        # type: (Optional[str], Optional[BackButtonBehavior_46c3eb02], Optional[Image_1942d978], Optional[str], Optional[TextContent_1d3959d5]) -> None
        """

        :param token: 
        :type token: (optional) str
        :param back_button: 
        :type back_button: (optional) ask_sdk_model.interfaces.display.back_button_behavior.BackButtonBehavior
        :param background_image: 
        :type background_image: (optional) ask_sdk_model.interfaces.display.image.Image
        :param title: 
        :type title: (optional) str
        :param text_content: 
        :type text_content: (optional) ask_sdk_model.interfaces.display.text_content.TextContent
        """
        self.__discriminator_value = "BodyTemplate1"  # type: str

        self.object_type = self.__discriminator_value
        super(BodyTemplate1, self).__init__(object_type=self.__discriminator_value, token=token, back_button=back_button)
        self.background_image = background_image
        self.title = title
        self.text_content = text_content

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
        if not isinstance(other, BodyTemplate1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
