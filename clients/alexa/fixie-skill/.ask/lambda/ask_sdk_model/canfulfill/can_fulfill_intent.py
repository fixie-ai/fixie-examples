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
    from ask_sdk_model.canfulfill.can_fulfill_intent_values import CanFulfillIntentValues as CanFulfillIntentValues_912ef433
    from ask_sdk_model.canfulfill.can_fulfill_slot import CanFulfillSlot as CanFulfillSlot_d32230a2


class CanFulfillIntent(object):
    """
    CanFulfillIntent represents the response to canFulfillIntentRequest includes the details about whether the skill can understand and fulfill the intent request with detected slots.


    :param can_fulfill: 
    :type can_fulfill: (optional) ask_sdk_model.canfulfill.can_fulfill_intent_values.CanFulfillIntentValues
    :param slots: A map that represents skill&#39;s detailed response to each detected slot within the intent such as if skill can understand and fulfill the detected slot. This supplements the overall canFulfillIntent response and help Alexa make better ranking and arbitration decisions. The key is the name of the slot. The value is an object of type CanFulfillSlot.
    :type slots: (optional) dict(str, ask_sdk_model.canfulfill.can_fulfill_slot.CanFulfillSlot)

    """
    deserialized_types = {
        'can_fulfill': 'ask_sdk_model.canfulfill.can_fulfill_intent_values.CanFulfillIntentValues',
        'slots': 'dict(str, ask_sdk_model.canfulfill.can_fulfill_slot.CanFulfillSlot)'
    }  # type: Dict

    attribute_map = {
        'can_fulfill': 'canFulfill',
        'slots': 'slots'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, can_fulfill=None, slots=None):
        # type: (Optional[CanFulfillIntentValues_912ef433], Optional[Dict[str, CanFulfillSlot_d32230a2]]) -> None
        """CanFulfillIntent represents the response to canFulfillIntentRequest includes the details about whether the skill can understand and fulfill the intent request with detected slots.

        :param can_fulfill: 
        :type can_fulfill: (optional) ask_sdk_model.canfulfill.can_fulfill_intent_values.CanFulfillIntentValues
        :param slots: A map that represents skill&#39;s detailed response to each detected slot within the intent such as if skill can understand and fulfill the detected slot. This supplements the overall canFulfillIntent response and help Alexa make better ranking and arbitration decisions. The key is the name of the slot. The value is an object of type CanFulfillSlot.
        :type slots: (optional) dict(str, ask_sdk_model.canfulfill.can_fulfill_slot.CanFulfillSlot)
        """
        self.__discriminator_value = None  # type: str

        self.can_fulfill = can_fulfill
        self.slots = slots

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
        if not isinstance(other, CanFulfillIntent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
