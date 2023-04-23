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
    from ask_sdk_model.device import Device as Device_8c07abbe
    from ask_sdk_model.interfaces.system_unit.unit import Unit as Unit_14958eb0
    from ask_sdk_model.application import Application as Application_fbe81c42
    from ask_sdk_model.user import User as User_8987f2de
    from ask_sdk_model.person import Person as Person_a00fdede


class SystemState(object):
    """

    :param application: 
    :type application: (optional) ask_sdk_model.application.Application
    :param user: 
    :type user: (optional) ask_sdk_model.user.User
    :param device: 
    :type device: (optional) ask_sdk_model.device.Device
    :param person: 
    :type person: (optional) ask_sdk_model.person.Person
    :param unit: 
    :type unit: (optional) ask_sdk_model.interfaces.system_unit.unit.Unit
    :param api_endpoint: A string that references the correct base URI to refer to by region, for use with APIs such as the Device Location API and Progressive Response API.
    :type api_endpoint: (optional) str
    :param api_access_token: A bearer token string that can be used by the skill (during the skill session) to access Alexa APIs resources of the registered Alexa customer and/or person who is making the request. This token encapsulates the permissions authorized under the registered Alexa account and device, and (optionally) the recognized person. Some resources, such as name or email, require explicit customer consent.\&quot; 
    :type api_access_token: (optional) str

    """
    deserialized_types = {
        'application': 'ask_sdk_model.application.Application',
        'user': 'ask_sdk_model.user.User',
        'device': 'ask_sdk_model.device.Device',
        'person': 'ask_sdk_model.person.Person',
        'unit': 'ask_sdk_model.interfaces.system_unit.unit.Unit',
        'api_endpoint': 'str',
        'api_access_token': 'str'
    }  # type: Dict

    attribute_map = {
        'application': 'application',
        'user': 'user',
        'device': 'device',
        'person': 'person',
        'unit': 'unit',
        'api_endpoint': 'apiEndpoint',
        'api_access_token': 'apiAccessToken'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, application=None, user=None, device=None, person=None, unit=None, api_endpoint=None, api_access_token=None):
        # type: (Optional[Application_fbe81c42], Optional[User_8987f2de], Optional[Device_8c07abbe], Optional[Person_a00fdede], Optional[Unit_14958eb0], Optional[str], Optional[str]) -> None
        """

        :param application: 
        :type application: (optional) ask_sdk_model.application.Application
        :param user: 
        :type user: (optional) ask_sdk_model.user.User
        :param device: 
        :type device: (optional) ask_sdk_model.device.Device
        :param person: 
        :type person: (optional) ask_sdk_model.person.Person
        :param unit: 
        :type unit: (optional) ask_sdk_model.interfaces.system_unit.unit.Unit
        :param api_endpoint: A string that references the correct base URI to refer to by region, for use with APIs such as the Device Location API and Progressive Response API.
        :type api_endpoint: (optional) str
        :param api_access_token: A bearer token string that can be used by the skill (during the skill session) to access Alexa APIs resources of the registered Alexa customer and/or person who is making the request. This token encapsulates the permissions authorized under the registered Alexa account and device, and (optionally) the recognized person. Some resources, such as name or email, require explicit customer consent.\&quot; 
        :type api_access_token: (optional) str
        """
        self.__discriminator_value = None  # type: str

        self.application = application
        self.user = user
        self.device = device
        self.person = person
        self.unit = unit
        self.api_endpoint = api_endpoint
        self.api_access_token = api_access_token

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
        if not isinstance(other, SystemState):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
