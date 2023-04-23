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
    from ask_sdk_model.ui.reprompt import Reprompt as Reprompt_ffee6ea4
    from ask_sdk_model.directive import Directive as Directive_e3e6b000
    from ask_sdk_model.interfaces.alexa.experimentation.experiment_trigger_response import ExperimentTriggerResponse as ExperimentTriggerResponse_5daea3f3
    from ask_sdk_model.canfulfill.can_fulfill_intent import CanFulfillIntent as CanFulfillIntent_8d777e62
    from ask_sdk_model.ui.output_speech import OutputSpeech as OutputSpeech_a070f8fb
    from ask_sdk_model.ui.card import Card as Card_3a03f3c4


class Response(object):
    """

    :param output_speech: 
    :type output_speech: (optional) ask_sdk_model.ui.output_speech.OutputSpeech
    :param card: 
    :type card: (optional) ask_sdk_model.ui.card.Card
    :param reprompt: 
    :type reprompt: (optional) ask_sdk_model.ui.reprompt.Reprompt
    :param directives: 
    :type directives: (optional) list[ask_sdk_model.directive.Directive]
    :param api_response: API response object containing API response value(s)
    :type api_response: (optional) object
    :param should_end_session: 
    :type should_end_session: (optional) bool
    :param can_fulfill_intent: 
    :type can_fulfill_intent: (optional) ask_sdk_model.canfulfill.can_fulfill_intent.CanFulfillIntent
    :param experimentation: Experiment trigger response from skill
    :type experimentation: (optional) ask_sdk_model.interfaces.alexa.experimentation.experiment_trigger_response.ExperimentTriggerResponse

    """
    deserialized_types = {
        'output_speech': 'ask_sdk_model.ui.output_speech.OutputSpeech',
        'card': 'ask_sdk_model.ui.card.Card',
        'reprompt': 'ask_sdk_model.ui.reprompt.Reprompt',
        'directives': 'list[ask_sdk_model.directive.Directive]',
        'api_response': 'object',
        'should_end_session': 'bool',
        'can_fulfill_intent': 'ask_sdk_model.canfulfill.can_fulfill_intent.CanFulfillIntent',
        'experimentation': 'ask_sdk_model.interfaces.alexa.experimentation.experiment_trigger_response.ExperimentTriggerResponse'
    }  # type: Dict

    attribute_map = {
        'output_speech': 'outputSpeech',
        'card': 'card',
        'reprompt': 'reprompt',
        'directives': 'directives',
        'api_response': 'apiResponse',
        'should_end_session': 'shouldEndSession',
        'can_fulfill_intent': 'canFulfillIntent',
        'experimentation': 'experimentation'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, output_speech=None, card=None, reprompt=None, directives=None, api_response=None, should_end_session=None, can_fulfill_intent=None, experimentation=None):
        # type: (Optional[OutputSpeech_a070f8fb], Optional[Card_3a03f3c4], Optional[Reprompt_ffee6ea4], Optional[List[Directive_e3e6b000]], Optional[object], Optional[bool], Optional[CanFulfillIntent_8d777e62], Optional[ExperimentTriggerResponse_5daea3f3]) -> None
        """

        :param output_speech: 
        :type output_speech: (optional) ask_sdk_model.ui.output_speech.OutputSpeech
        :param card: 
        :type card: (optional) ask_sdk_model.ui.card.Card
        :param reprompt: 
        :type reprompt: (optional) ask_sdk_model.ui.reprompt.Reprompt
        :param directives: 
        :type directives: (optional) list[ask_sdk_model.directive.Directive]
        :param api_response: API response object containing API response value(s)
        :type api_response: (optional) object
        :param should_end_session: 
        :type should_end_session: (optional) bool
        :param can_fulfill_intent: 
        :type can_fulfill_intent: (optional) ask_sdk_model.canfulfill.can_fulfill_intent.CanFulfillIntent
        :param experimentation: Experiment trigger response from skill
        :type experimentation: (optional) ask_sdk_model.interfaces.alexa.experimentation.experiment_trigger_response.ExperimentTriggerResponse
        """
        self.__discriminator_value = None  # type: str

        self.output_speech = output_speech
        self.card = card
        self.reprompt = reprompt
        self.directives = directives
        self.api_response = api_response
        self.should_end_session = should_end_session
        self.can_fulfill_intent = can_fulfill_intent
        self.experimentation = experimentation

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
        if not isinstance(other, Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
