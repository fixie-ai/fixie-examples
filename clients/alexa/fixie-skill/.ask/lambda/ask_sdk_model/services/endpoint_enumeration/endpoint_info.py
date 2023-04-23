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
    from ask_sdk_model.services.endpoint_enumeration.endpoint_capability import EndpointCapability as EndpointCapability_afc63a4a


class EndpointInfo(object):
    """
    Contains the list of connected endpoints and their declared capabilities.


    :param endpoint_id: A unique identifier for the endpoint.
    :type endpoint_id: (optional) str
    :param friendly_name: The name of the endpoint. Because this name might be changed by the user or the platform, it might be different than the Bluetooth friendly name.
    :type friendly_name: (optional) str
    :param capabilities: The list of endpoint capabilities.
    :type capabilities: (optional) list[ask_sdk_model.services.endpoint_enumeration.endpoint_capability.EndpointCapability]

    """
    deserialized_types = {
        'endpoint_id': 'str',
        'friendly_name': 'str',
        'capabilities': 'list[ask_sdk_model.services.endpoint_enumeration.endpoint_capability.EndpointCapability]'
    }  # type: Dict

    attribute_map = {
        'endpoint_id': 'endpointId',
        'friendly_name': 'friendlyName',
        'capabilities': 'capabilities'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, endpoint_id=None, friendly_name=None, capabilities=None):
        # type: (Optional[str], Optional[str], Optional[List[EndpointCapability_afc63a4a]]) -> None
        """Contains the list of connected endpoints and their declared capabilities.

        :param endpoint_id: A unique identifier for the endpoint.
        :type endpoint_id: (optional) str
        :param friendly_name: The name of the endpoint. Because this name might be changed by the user or the platform, it might be different than the Bluetooth friendly name.
        :type friendly_name: (optional) str
        :param capabilities: The list of endpoint capabilities.
        :type capabilities: (optional) list[ask_sdk_model.services.endpoint_enumeration.endpoint_capability.EndpointCapability]
        """
        self.__discriminator_value = None  # type: str

        self.endpoint_id = endpoint_id
        self.friendly_name = friendly_name
        self.capabilities = capabilities

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
        if not isinstance(other, EndpointInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
