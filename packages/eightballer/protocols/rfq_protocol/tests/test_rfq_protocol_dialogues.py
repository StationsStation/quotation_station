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

"""Test dialogues module for rfq_protocol protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.rfq_protocol.custom_types import RequestForQuote
from packages.eightballer.protocols.rfq_protocol.dialogues import (
    RfqProtocolDialogue,
    RfqProtocolDialogues,
)
from packages.eightballer.protocols.rfq_protocol.message import RfqProtocolMessage


class TestDialoguesRfqProtocol(BaseProtocolDialoguesTestCase):
    """Test for the 'rfq_protocol' protocol dialogues."""

    MESSAGE_CLASS = RfqProtocolMessage

    DIALOGUE_CLASS = RfqProtocolDialogue

    DIALOGUES_CLASS = RfqProtocolDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = RfqProtocolDialogue.Role.BUYER  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=RfqProtocolMessage.Performative.CREATE_RFQ,
            rfq=RequestForQuote(),  # check it please!
        )
