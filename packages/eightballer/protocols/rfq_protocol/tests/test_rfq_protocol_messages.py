# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Test messages module for rfq_protocol protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase
from packages.eightballer.protocols.rfq_protocol.message import RfqProtocolMessage
from packages.eightballer.protocols.rfq_protocol.custom_types import (
    Quote,
    RFQError,
    RequestForQuote,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageRfqProtocol(BaseProtocolMessagesTestCase):
    """Test for the 'rfq_protocol' protocol message."""

    MESSAGE_CLASS = RfqProtocolMessage

    def build_messages(self) -> List[RfqProtocolMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.CREATE_RFQ,
                rfq=RequestForQuote(**load_data("RequestForQuote")),  # check it please!
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.QUOTATION,
                rfq=RequestForQuote(**load_data("RequestForQuote")),  # check it please!
                quote=Quote(**load_data("Quote")),  # check it please!
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.RFQ_ERROR,
                error_code=RFQError(0),  # check it please!
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.ACCEPT,
                quote=Quote(**load_data("Quote")),  # check it please!
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.DECLINE,
                quote=Quote(**load_data("Quote")),  # check it please!
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP,
                quote=Quote(**load_data("Quote")),  # check it please!
                seller_address="some str",
                swap_id="some str",
                secret_hash="some str",
                secret="some str",
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP,
                swap_id="some str",
                secret="some str",
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.BUYER_CLAIM,
                secret="some str",
                chain_id="some str",
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.SELLER_CLAIM,
                secret="some str",
                chain_id="some str",
            ),
        ]

    def build_inconsistent(self) -> List[RfqProtocolMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.CREATE_RFQ,
                # skip content: rfq
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.QUOTATION,
                # skip content: rfq
                quote=Quote(**load_data("Quote")),  # check it please!
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.RFQ_ERROR,
                # skip content: error_code
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.ACCEPT,
                # skip content: quote
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.DECLINE,
                # skip content: quote
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP,
                # skip content: quote
                seller_address="some str",
                swap_id="some str",
                secret_hash="some str",
                secret="some str",
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP,
                # skip content: swap_id
                secret="some str",
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.BUYER_CLAIM,
                # skip content: secret
                chain_id="some str",
            ),
            RfqProtocolMessage(
                performative=RfqProtocolMessage.Performative.SELLER_CLAIM,
                # skip content: secret
                chain_id="some str",
            ),
        ]
