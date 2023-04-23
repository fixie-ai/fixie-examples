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
    from ask_sdk_model.interfaces.alexa.presentation.html.transformer import Transformer as Transformer_8371ca46


class HandleMessageDirective(Directive):
    """
    The HandleMessage directive sends a message to a skill&#39;s web application that runs on the device browser. 


    :param message: A free-form object containing data to deliver to a skill&#39;s HTML application running the device. Maximum size 18 KB.
    :type message: (optional) object
    :param transformers: An array of objects for performing text-to-speech transformations with message data
    :type transformers: (optional) list[ask_sdk_model.interfaces.alexa.presentation.html.transformer.Transformer]

    """
    deserialized_types = {
        'object_type': 'str',
        'message': 'object',
        'transformers': 'list[ask_sdk_model.interfaces.alexa.presentation.html.transformer.Transformer]'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'message': 'message',
        'transformers': 'transformers'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, message=None, transformers=None):
        # type: (Optional[object], Optional[List[Transformer_8371ca46]]) -> None
        """The HandleMessage directive sends a message to a skill&#39;s web application that runs on the device browser. 

        :param message: A free-form object containing data to deliver to a skill&#39;s HTML application running the device. Maximum size 18 KB.
        :type message: (optional) object
        :param transformers: An array of objects for performing text-to-speech transformations with message data
        :type transformers: (optional) list[ask_sdk_model.interfaces.alexa.presentation.html.transformer.Transformer]
        """
        self.__discriminator_value = "Alexa.Presentation.HTML.HandleMessage"  # type: str

        self.object_type = self.__discriminator_value
        super(HandleMessageDirective, self).__init__(object_type=self.__discriminator_value)
        self.message = message
        self.transformers = transformers

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
        if not isinstance(other, HandleMessageDirective):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
