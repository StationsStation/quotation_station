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

"""
This module contains the classes required for rfq_protocol dialogue management.

- RfqProtocolDialogue: The dialogue class maintains state of a dialogue and manages it.
- RfqProtocolDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, Dict, FrozenSet, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues

from packages.eightballer.protocols.rfq_protocol.message import RfqProtocolMessage


class RfqProtocolDialogue(Dialogue):
    """The rfq_protocol dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {RfqProtocolMessage.Performative.CREATE_RFQ}
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            RfqProtocolMessage.Performative.DECLINE,
            RfqProtocolMessage.Performative.BUYER_CLAIM,
            RfqProtocolMessage.Performative.SELLER_CLAIM,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        RfqProtocolMessage.Performative.ACCEPT: frozenset(
            {RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP}
        ),
        RfqProtocolMessage.Performative.BUYER_CLAIM: frozenset(),
        RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP: frozenset(
            {
                RfqProtocolMessage.Performative.BUYER_CLAIM,
                RfqProtocolMessage.Performative.SELLER_CLAIM,
            }
        ),
        RfqProtocolMessage.Performative.CREATE_RFQ: frozenset(
            {
                RfqProtocolMessage.Performative.QUOTATION,
                RfqProtocolMessage.Performative.RFQ_ERROR,
            }
        ),
        RfqProtocolMessage.Performative.DECLINE: frozenset(),
        RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP: frozenset(
            {RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP}
        ),
        RfqProtocolMessage.Performative.QUOTATION: frozenset(
            {
                RfqProtocolMessage.Performative.ACCEPT,
                RfqProtocolMessage.Performative.DECLINE,
            }
        ),
        RfqProtocolMessage.Performative.RFQ_ERROR: frozenset(
            {RfqProtocolMessage.Performative.DECLINE}
        ),
        RfqProtocolMessage.Performative.SELLER_CLAIM: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a rfq_protocol dialogue."""

        BUYER = "buyer"
        SELLER = "seller"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a rfq_protocol dialogue."""

        DECLINE = 0
        BUYER_CLAIM = 1
        SELLER_CLAIM = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[RfqProtocolMessage] = RfqProtocolMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :param message_class: the message class used
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class RfqProtocolDialogues(Dialogues, ABC):
    """This class keeps track of all rfq_protocol dialogues."""

    END_STATES = frozenset(
        {
            RfqProtocolDialogue.EndState.DECLINE,
            RfqProtocolDialogue.EndState.BUYER_CLAIM,
            RfqProtocolDialogue.EndState.SELLER_CLAIM,
        }
    )

    _keep_terminal_state_dialogues = False

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[RfqProtocolDialogue] = RfqProtocolDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=RfqProtocolMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
