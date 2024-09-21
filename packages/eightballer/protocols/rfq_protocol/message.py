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

"""This module contains rfq_protocol's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.rfq_protocol.custom_types import (
    Quote as CustomQuote,
)
from packages.eightballer.protocols.rfq_protocol.custom_types import (
    RFQError as CustomRFQError,
)
from packages.eightballer.protocols.rfq_protocol.custom_types import (
    RequestForQuote as CustomRequestForQuote,
)


_default_logger = logging.getLogger(
    "aea.packages.eightballer.protocols.rfq_protocol.message"
)

DEFAULT_BODY_SIZE = 4


class RfqProtocolMessage(Message):
    """A protocol for representing a request for quotation (RFQ) in the the quotation negotiation dialogue."""

    protocol_id = PublicId.from_str("eightballer/rfq_protocol:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/rfq_protocol:0.1.0")

    Quote = CustomQuote

    RFQError = CustomRFQError

    RequestForQuote = CustomRequestForQuote

    class Performative(Message.Performative):
        """Performatives for the rfq_protocol protocol."""

        ACCEPT = "accept"
        BUYER_CLAIM = "buyer_claim"
        COMPLETE_ATOMIC_SWAP = "complete_atomic_swap"
        CREATE_RFQ = "create_rfq"
        DECLINE = "decline"
        INITIATE_ATOMIC_SWAP = "initiate_atomic_swap"
        QUOTATION = "quotation"
        RFQ_ERROR = "rfq_error"
        SELLER_CLAIM = "seller_claim"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "accept",
        "buyer_claim",
        "complete_atomic_swap",
        "create_rfq",
        "decline",
        "initiate_atomic_swap",
        "quotation",
        "rfq_error",
        "seller_claim",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "chain_id",
            "dialogue_reference",
            "error_code",
            "message_id",
            "performative",
            "quote",
            "rfq",
            "secret",
            "secret_hash",
            "seller_address",
            "swap_id",
            "target",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of RfqProtocolMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        :param **kwargs: extra options.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=RfqProtocolMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(RfqProtocolMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def chain_id(self) -> str:
        """Get the 'chain_id' content from the message."""
        enforce(self.is_set("chain_id"), "'chain_id' content is not set.")
        return cast(str, self.get("chain_id"))

    @property
    def error_code(self) -> CustomRFQError:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomRFQError, self.get("error_code"))

    @property
    def quote(self) -> CustomQuote:
        """Get the 'quote' content from the message."""
        enforce(self.is_set("quote"), "'quote' content is not set.")
        return cast(CustomQuote, self.get("quote"))

    @property
    def rfq(self) -> CustomRequestForQuote:
        """Get the 'rfq' content from the message."""
        enforce(self.is_set("rfq"), "'rfq' content is not set.")
        return cast(CustomRequestForQuote, self.get("rfq"))

    @property
    def secret(self) -> str:
        """Get the 'secret' content from the message."""
        enforce(self.is_set("secret"), "'secret' content is not set.")
        return cast(str, self.get("secret"))

    @property
    def secret_hash(self) -> str:
        """Get the 'secret_hash' content from the message."""
        enforce(self.is_set("secret_hash"), "'secret_hash' content is not set.")
        return cast(str, self.get("secret_hash"))

    @property
    def seller_address(self) -> str:
        """Get the 'seller_address' content from the message."""
        enforce(self.is_set("seller_address"), "'seller_address' content is not set.")
        return cast(str, self.get("seller_address"))

    @property
    def swap_id(self) -> str:
        """Get the 'swap_id' content from the message."""
        enforce(self.is_set("swap_id"), "'swap_id' content is not set.")
        return cast(str, self.get("swap_id"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the rfq_protocol protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                    type(self.message_id)
                ),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                    type(self.target)
                ),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, RfqProtocolMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == RfqProtocolMessage.Performative.CREATE_RFQ:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.rfq, CustomRequestForQuote),
                    "Invalid type for content 'rfq'. Expected 'RequestForQuote'. Found '{}'.".format(
                        type(self.rfq)
                    ),
                )
            elif self.performative == RfqProtocolMessage.Performative.QUOTATION:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.rfq, CustomRequestForQuote),
                    "Invalid type for content 'rfq'. Expected 'RequestForQuote'. Found '{}'.".format(
                        type(self.rfq)
                    ),
                )
                enforce(
                    isinstance(self.quote, CustomQuote),
                    "Invalid type for content 'quote'. Expected 'Quote'. Found '{}'.".format(
                        type(self.quote)
                    ),
                )
            elif self.performative == RfqProtocolMessage.Performative.RFQ_ERROR:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.error_code, CustomRFQError),
                    "Invalid type for content 'error_code'. Expected 'RFQError'. Found '{}'.".format(
                        type(self.error_code)
                    ),
                )
            elif self.performative == RfqProtocolMessage.Performative.ACCEPT:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.quote, CustomQuote),
                    "Invalid type for content 'quote'. Expected 'Quote'. Found '{}'.".format(
                        type(self.quote)
                    ),
                )
            elif self.performative == RfqProtocolMessage.Performative.DECLINE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.quote, CustomQuote),
                    "Invalid type for content 'quote'. Expected 'Quote'. Found '{}'.".format(
                        type(self.quote)
                    ),
                )
            elif (
                self.performative
                == RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP
            ):
                expected_nb_of_contents = 5
                enforce(
                    isinstance(self.quote, CustomQuote),
                    "Invalid type for content 'quote'. Expected 'Quote'. Found '{}'.".format(
                        type(self.quote)
                    ),
                )
                enforce(
                    isinstance(self.seller_address, str),
                    "Invalid type for content 'seller_address'. Expected 'str'. Found '{}'.".format(
                        type(self.seller_address)
                    ),
                )
                enforce(
                    isinstance(self.swap_id, str),
                    "Invalid type for content 'swap_id'. Expected 'str'. Found '{}'.".format(
                        type(self.swap_id)
                    ),
                )
                enforce(
                    isinstance(self.secret_hash, str),
                    "Invalid type for content 'secret_hash'. Expected 'str'. Found '{}'.".format(
                        type(self.secret_hash)
                    ),
                )
                enforce(
                    isinstance(self.secret, str),
                    "Invalid type for content 'secret'. Expected 'str'. Found '{}'.".format(
                        type(self.secret)
                    ),
                )
            elif (
                self.performative
                == RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP
            ):
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.swap_id, str),
                    "Invalid type for content 'swap_id'. Expected 'str'. Found '{}'.".format(
                        type(self.swap_id)
                    ),
                )
                enforce(
                    isinstance(self.secret, str),
                    "Invalid type for content 'secret'. Expected 'str'. Found '{}'.".format(
                        type(self.secret)
                    ),
                )
            elif self.performative == RfqProtocolMessage.Performative.BUYER_CLAIM:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.secret, str),
                    "Invalid type for content 'secret'. Expected 'str'. Found '{}'.".format(
                        type(self.secret)
                    ),
                )
                enforce(
                    isinstance(self.chain_id, str),
                    "Invalid type for content 'chain_id'. Expected 'str'. Found '{}'.".format(
                        type(self.chain_id)
                    ),
                )
            elif self.performative == RfqProtocolMessage.Performative.SELLER_CLAIM:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.secret, str),
                    "Invalid type for content 'secret'. Expected 'str'. Found '{}'.".format(
                        type(self.secret)
                    ),
                )
                enforce(
                    isinstance(self.chain_id, str),
                    "Invalid type for content 'chain_id'. Expected 'str'. Found '{}'.".format(
                        type(self.chain_id)
                    ),
                )

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                        self.target
                    ),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
