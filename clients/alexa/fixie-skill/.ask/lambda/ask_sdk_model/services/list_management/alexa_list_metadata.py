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
    from ask_sdk_model.services.list_management.status import Status as Status_bac65d64
    from ask_sdk_model.services.list_management.list_state import ListState as ListState_7568bb1f


class AlexaListMetadata(object):
    """

    :param list_id: 
    :type list_id: (optional) str
    :param name: 
    :type name: (optional) str
    :param state: 
    :type state: (optional) ask_sdk_model.services.list_management.list_state.ListState
    :param version: 
    :type version: (optional) int
    :param status_map: 
    :type status_map: (optional) list[ask_sdk_model.services.list_management.status.Status]

    """
    deserialized_types = {
        'list_id': 'str',
        'name': 'str',
        'state': 'ask_sdk_model.services.list_management.list_state.ListState',
        'version': 'int',
        'status_map': 'list[ask_sdk_model.services.list_management.status.Status]'
    }  # type: Dict

    attribute_map = {
        'list_id': 'listId',
        'name': 'name',
        'state': 'state',
        'version': 'version',
        'status_map': 'statusMap'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, list_id=None, name=None, state=None, version=None, status_map=None):
        # type: (Optional[str], Optional[str], Optional[ListState_7568bb1f], Optional[int], Optional[List[Status_bac65d64]]) -> None
        """

        :param list_id: 
        :type list_id: (optional) str
        :param name: 
        :type name: (optional) str
        :param state: 
        :type state: (optional) ask_sdk_model.services.list_management.list_state.ListState
        :param version: 
        :type version: (optional) int
        :param status_map: 
        :type status_map: (optional) list[ask_sdk_model.services.list_management.status.Status]
        """
        self.__discriminator_value = None  # type: str

        self.list_id = list_id
        self.name = name
        self.state = state
        self.version = version
        self.status_map = status_map

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
        if not isinstance(other, AlexaListMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
