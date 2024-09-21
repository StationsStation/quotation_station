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
    CollectSameUntilThresholdRound,
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


class TxState(Enum):
    PRE_TRANSACTION = "pre_transaction"
    POST_NEW_SWAP = "post_new_swap"
    POST_CLAIM = "post_claim"
    POST_REFUND = "post_refund"


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

    @property
    def most_voted_tx_hash(self) -> float:
        """Get the most_voted_tx_hash."""
        return cast(float, self.db.get_strict("most_voted_tx_hash"))

    @property
    def rfq_expired(self) -> bool:
        return self.db.get("rfq_expired", False)

    @property
    def tx_state(self) -> TxState:
        """Get the transaction state."""
        return self.db.get("tx_state", None)


class CollectExchangeDataRound(CollectSameUntilThresholdRound):
    """CollectExchangeDataRound"""

    payload_class = CollectExchangeDataPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        return self.synchronized_data, Event.DONE


class AwaitRFQsRound(CollectSameUntilThresholdRound):
    """AwaitRFQsRound"""

    payload_class = AwaitRFQsPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        return self.synchronized_data, Event.QUOTE_ACCEPTED


class PrepareSupplyTransactionRound(CollectSameUntilThresholdRound):
    """PrepareSupplyTransactionRound"""

    payload_class = PrepareSupplyTransactionPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if self.context.params.executor_mode.value == "EOA":
            return self.synchronized_data, Event.FINALISED

        return self.synchronized_data, Event.DONE


class AwaitBuyerTransactionsRound(CollectSameUntilThresholdRound):
    """AwaitBuyerTransactionsRound"""

    payload_class = AwaitBuyerTransactionsPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if self.synchronized_data.rfq_expired:
            return self.synchronized_data, Event.RFQ_EXPIRED

        return self.synchronized_data, Event.DONE


class PrepareClaimTransactionsRound(CollectSameUntilThresholdRound):
    """PrepareClaimTransactionsRound"""

    payload_class = PrepareClaimTransactionsPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if (self.synchronized_data.tx_state == TxState.POST_CLAIM
            or self.context.params.executor_mode.value == "EOA"):
            return self.synchronized_data, Event.FINALISED

        self.synchronized_data.tx_state = TxState.POST_CLAIM
        return self.synchronized_data, Event.DONE


class PrepareRefundTransactionsRound(CollectSameUntilThresholdRound):
    """PrepareRefundTransactionsRound"""

    payload_class = PrepareRefundTransactionsPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if (self.synchronized_data.tx_state == TxState.POST_REFUND
            or self.params.executor_setup.execution_mode.value == "EOA"):
            # self.tx_state = TxState.PRE_TRANSACTION
            return self.synchronized_data, Event.FINALISED

        return self.synchronized_data, Event.DONE

class PostTransactionRound(CollectSameUntilThresholdRound):
    """PostTransactionRound"""

    payload_class = PostTransactionPayload
    payload_attribute = "content"
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        tx_state = self.synchronized_data.tx_state
        if tx_state == TxState.POST_NEW_SWAP:
            return self.synchronized_data, Event.POST_NEW_SWAP
        elif tx_state == TxState.POST_CLAIM:
            return self.synchronized_data, Event.POST_CLAIM
        elif tx_state == TxState.POST_REFUND:
            return self.synchronized_data, Event.POST_REFUND
        raise ValueError(f"FSM design error, incorrect transation state: {tx_state}")



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
        PostTransactionRound: {"participants"},
        CollectExchangeDataRound: {"participants"},
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        SuccessfulExecutionRound: {"most_voted_tx_hash"},
        UnSuccessfulExecutionRound: set(),
        FinalisedRefundTransactionsRound: {"most_voted_tx_hash"},
        FinalisedClaimTransactionsRound: {"most_voted_tx_hash"},
        FinalisedSupplyTransactionsRound: {"most_voted_tx_hash"},
    }
