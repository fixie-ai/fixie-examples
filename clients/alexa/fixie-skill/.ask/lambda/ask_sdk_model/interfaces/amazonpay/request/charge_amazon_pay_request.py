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
from ask_sdk_model.interfaces.amazonpay.model.request.base_amazon_pay_entity import BaseAmazonPayEntity


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.interfaces.amazonpay.model.request.provider_attributes import ProviderAttributes as ProviderAttributes_32296063
    from ask_sdk_model.interfaces.amazonpay.model.request.authorize_attributes import AuthorizeAttributes as AuthorizeAttributes_2defaf71
    from ask_sdk_model.interfaces.amazonpay.model.request.payment_action import PaymentAction as PaymentAction_974ab70f
    from ask_sdk_model.interfaces.amazonpay.model.request.seller_order_attributes import SellerOrderAttributes as SellerOrderAttributes_48ed79ae


class ChargeAmazonPayRequest(BaseAmazonPayEntity):
    """
    Charge Amazon Pay Request Object.


    :param version: Version of the Amazon Pay Entity. Can be 1 or greater.
    :type version: (optional) str
    :param seller_id: The seller ID (also known as merchant ID). If you are an Ecommerce Provider (Solution Provider), please specify the ID of the merchant, not your provider ID.
    :type seller_id: (optional) str
    :param billing_agreement_id: The payment contract i.e. billing agreement created for the user.
    :type billing_agreement_id: (optional) str
    :param payment_action: 
    :type payment_action: (optional) ask_sdk_model.interfaces.amazonpay.model.request.payment_action.PaymentAction
    :param authorize_attributes: 
    :type authorize_attributes: (optional) ask_sdk_model.interfaces.amazonpay.model.request.authorize_attributes.AuthorizeAttributes
    :param seller_order_attributes: 
    :type seller_order_attributes: (optional) ask_sdk_model.interfaces.amazonpay.model.request.seller_order_attributes.SellerOrderAttributes
    :param provider_attributes: 
    :type provider_attributes: (optional) ask_sdk_model.interfaces.amazonpay.model.request.provider_attributes.ProviderAttributes

    """
    deserialized_types = {
        'object_type': 'str',
        'version': 'str',
        'seller_id': 'str',
        'billing_agreement_id': 'str',
        'payment_action': 'ask_sdk_model.interfaces.amazonpay.model.request.payment_action.PaymentAction',
        'authorize_attributes': 'ask_sdk_model.interfaces.amazonpay.model.request.authorize_attributes.AuthorizeAttributes',
        'seller_order_attributes': 'ask_sdk_model.interfaces.amazonpay.model.request.seller_order_attributes.SellerOrderAttributes',
        'provider_attributes': 'ask_sdk_model.interfaces.amazonpay.model.request.provider_attributes.ProviderAttributes'
    }  # type: Dict

    attribute_map = {
        'object_type': '@type',
        'version': '@version',
        'seller_id': 'sellerId',
        'billing_agreement_id': 'billingAgreementId',
        'payment_action': 'paymentAction',
        'authorize_attributes': 'authorizeAttributes',
        'seller_order_attributes': 'sellerOrderAttributes',
        'provider_attributes': 'providerAttributes'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, version=None, seller_id=None, billing_agreement_id=None, payment_action=None, authorize_attributes=None, seller_order_attributes=None, provider_attributes=None):
        # type: (Optional[str], Optional[str], Optional[str], Optional[PaymentAction_974ab70f], Optional[AuthorizeAttributes_2defaf71], Optional[SellerOrderAttributes_48ed79ae], Optional[ProviderAttributes_32296063]) -> None
        """Charge Amazon Pay Request Object.

        :param version: Version of the Amazon Pay Entity. Can be 1 or greater.
        :type version: (optional) str
        :param seller_id: The seller ID (also known as merchant ID). If you are an Ecommerce Provider (Solution Provider), please specify the ID of the merchant, not your provider ID.
        :type seller_id: (optional) str
        :param billing_agreement_id: The payment contract i.e. billing agreement created for the user.
        :type billing_agreement_id: (optional) str
        :param payment_action: 
        :type payment_action: (optional) ask_sdk_model.interfaces.amazonpay.model.request.payment_action.PaymentAction
        :param authorize_attributes: 
        :type authorize_attributes: (optional) ask_sdk_model.interfaces.amazonpay.model.request.authorize_attributes.AuthorizeAttributes
        :param seller_order_attributes: 
        :type seller_order_attributes: (optional) ask_sdk_model.interfaces.amazonpay.model.request.seller_order_attributes.SellerOrderAttributes
        :param provider_attributes: 
        :type provider_attributes: (optional) ask_sdk_model.interfaces.amazonpay.model.request.provider_attributes.ProviderAttributes
        """
        self.__discriminator_value = "ChargeAmazonPayRequest"  # type: str

        self.object_type = self.__discriminator_value
        super(ChargeAmazonPayRequest, self).__init__(object_type=self.__discriminator_value, version=version)
        self.seller_id = seller_id
        self.billing_agreement_id = billing_agreement_id
        self.payment_action = payment_action
        self.authorize_attributes = authorize_attributes
        self.seller_order_attributes = seller_order_attributes
        self.provider_attributes = provider_attributes

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
        if not isinstance(other, ChargeAmazonPayRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
