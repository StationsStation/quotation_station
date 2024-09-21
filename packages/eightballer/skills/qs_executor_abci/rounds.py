# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 Valory AG
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

"""This package contains the rounds of QSExecutorAbciApp."""

from enum import Enum
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
)

from packages.eightballer.skills.qs_executor_abci.payloads import (
    AwaitBuyerTransactionsPayload,
    AwaitRFQsPayload,
    CollectExchangeDataPayload,
    PostTransactionPayload,
    PrepareClaimTransactionsPayload,
    PrepareRefundTransactionsPayload,
    PrepareSupplyTransactionPayload,
)


class Event(Enum):
    """QSExecutorAbciApp Events"""

    POST_NEW_SWAP = "post_new_swap"
    POST_REFUND = "post_refund"
    POST_CLAIM = "post_claim"
    RFQ_EXPIRED = "rfq_expired"
    DONE = "done"
    QUOTE_ACCEPTED = "quote_accepted"
    FINALISED = "finalised"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class AwaitBuyerTransactionsRound(AbstractRound):
    """AwaitBuyerTransactionsRound"""

    payload_class = AwaitBuyerTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: AwaitBuyerTransactionsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AwaitBuyerTransactionsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class AwaitRFQsRound(AbstractRound):
    """AwaitRFQsRound"""

    payload_class = AwaitRFQsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: AwaitRFQsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AwaitRFQsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class CollectExchangeDataRound(AbstractRound):
    """CollectExchangeDataRound"""

    payload_class = CollectExchangeDataPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: CollectExchangeDataPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CollectExchangeDataPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PostTransactionRound(AbstractRound):
    """PostTransactionRound"""

    payload_class = PostTransactionPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: PostTransactionPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PostTransactionPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PrepareClaimTransactionsRound(AbstractRound):
    """PrepareClaimTransactionsRound"""

    payload_class = PrepareClaimTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: PrepareClaimTransactionsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareClaimTransactionsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PrepareRefundTransactionsRound(AbstractRound):
    """PrepareRefundTransactionsRound"""

    payload_class = PrepareRefundTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: PrepareRefundTransactionsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareRefundTransactionsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PrepareSupplyTransactionRound(AbstractRound):
    """PrepareSupplyTransactionRound"""

    payload_class = PrepareSupplyTransactionPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: PrepareSupplyTransactionPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareSupplyTransactionPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class FinalisedClaimTransactionsRound(DegenerateRound):
    """FinalisedClaimTransactionsRound"""


class FinalisedRefundTransactionsRound(DegenerateRound):
    """FinalisedRefundTransactionsRound"""


class FinalisedSupplyTransactionsRound(DegenerateRound):
    """FinalisedSupplyTransactionsRound"""


class SuccessfulExecutionRound(DegenerateRound):
    """SuccessfulExecutionRound"""


class UnSuccessfulExecutionRound(DegenerateRound):
    """UnSuccessfulExecutionRound"""


class QSExecutorAbciApp(AbciApp[Event]):
    """QSExecutorAbciApp"""

    initial_round_cls: AppState = PostTransactionRound
    initial_states: Set[AppState] = {PostTransactionRound, CollectExchangeDataRound}
    transition_function: AbciAppTransitionFunction = {
        AwaitBuyerTransactionsRound: {
            Event.DONE: PrepareClaimTransactionsRound,
            Event.RFQ_EXPIRED: PrepareRefundTransactionsRound
        },
        AwaitRFQsRound: {
            Event.QUOTE_ACCEPTED: PrepareSupplyTransactionRound
        },
        CollectExchangeDataRound: {
            Event.DONE: AwaitRFQsRound
        },
        PostTransactionRound: {
            Event.POST_CLAIM: SuccessfulExecutionRound,
            Event.POST_NEW_SWAP: AwaitBuyerTransactionsRound,
            Event.POST_REFUND: UnSuccessfulExecutionRound
        },
        PrepareClaimTransactionsRound: {
            Event.DONE: FinalisedClaimTransactionsRound,
            Event.FINALISED: SuccessfulExecutionRound
        },
        PrepareRefundTransactionsRound: {
            Event.DONE: FinalisedRefundTransactionsRound,
            Event.FINALISED: UnSuccessfulExecutionRound
        },
        PrepareSupplyTransactionRound: {
            Event.DONE: FinalisedSupplyTransactionsRound,
            Event.FINALISED: AwaitBuyerTransactionsRound
        },
        SuccessfulExecutionRound: {},
        UnSuccessfulExecutionRound: {},
        FinalisedSupplyTransactionsRound: {},
        FinalisedRefundTransactionsRound: {},
        FinalisedClaimTransactionsRound: {}
    }
    final_states: Set[AppState] = {SuccessfulExecutionRound, UnSuccessfulExecutionRound, FinalisedRefundTransactionsRound, FinalisedClaimTransactionsRound, FinalisedSupplyTransactionsRound}
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        PostTransactionRound: [],
    	CollectExchangeDataRound: [],
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        SuccessfulExecutionRound: [],
    	UnSuccessfulExecutionRound: [],
    	FinalisedRefundTransactionsRound: [],
    	FinalisedClaimTransactionsRound: [],
    	FinalisedSupplyTransactionsRound: [],
    }
