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
from ask_sdk_model.slot_value import SlotValue


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.slu.entityresolution.resolutions import Resolutions as Resolutions_e7d66a3


class SimpleSlotValue(SlotValue):
    """
    Slot value containing a single string value and resolutions.


    :param value: A string that represents the value the user spoke for the slot. This is the actual value the user spoke, not necessarily the canonical value or one of the synonyms defined for the entity. Note that AMAZON.LITERAL slot values sent to your service are always in all lower case.
    :type value: (optional) str
    :param resolutions: Contains the results of entity resolution. These are organized by authority. An authority represents the source for the data provided for the slot. For a custom slot type, the authority is the slot type you defined.
    :type resolutions: (optional) ask_sdk_model.slu.entityresolution.resolutions.Resolutions

    """
    deserialized_types = {
        'object_type': 'str',
        'value': 'str',
        'resolutions': 'ask_sdk_model.slu.entityresolution.resolutions.Resolutions'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'value': 'value',
        'resolutions': 'resolutions'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, value=None, resolutions=None):
        # type: (Optional[str], Optional[Resolutions_e7d66a3]) -> None
        """Slot value containing a single string value and resolutions.

        :param value: A string that represents the value the user spoke for the slot. This is the actual value the user spoke, not necessarily the canonical value or one of the synonyms defined for the entity. Note that AMAZON.LITERAL slot values sent to your service are always in all lower case.
        :type value: (optional) str
        :param resolutions: Contains the results of entity resolution. These are organized by authority. An authority represents the source for the data provided for the slot. For a custom slot type, the authority is the slot type you defined.
        :type resolutions: (optional) ask_sdk_model.slu.entityresolution.resolutions.Resolutions
        """
        self.__discriminator_value = "Simple"  # type: str

        self.object_type = self.__discriminator_value
        super(SimpleSlotValue, self).__init__(object_type=self.__discriminator_value)
        self.value = value
        self.resolutions = resolutions

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
        if not isinstance(other, SimpleSlotValue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
