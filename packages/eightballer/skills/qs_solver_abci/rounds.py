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

"""This package contains the rounds of QSSolverAbciApp."""

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

from packages.eightballer.skills.qs_solver_abci.payloads import (
    AwaitQuotesPayload,
    AwaitSupplierTransactionsPayload,
    AwaitingOpportunityPayload,
    PostTransactionPayload,
    PrepareClaimTransactionsPayload,
    PrepareNewSwapTransactionsPayload,
    PrepareRefundTransactionsPayload,
    SelectQuotesPayload,
    SubmitRFQPayload,
)


class TxState(Enum):
    PRE_TRANSACTION = "pre_transaction"
    POST_NEW_SWAP = "post_new_swap"
    POST_CLAIM = "post_claim"
    POST_REFUND = "post_refund"


class Event(Enum):
    """QSSolverAbciApp Events"""

    ACCEPT_QUOTES = "accept_quotes"
    TRIGGERED = "triggered"
    NO_QUOTES = "no_quotes"
    POST_NEW_SWAP = "post_new_swap"
    NOT_TRIGGERED = "not_triggered"
    QUOTES = "quotes"
    DONE = "done"
    FINALISED = "finalised"
    COUNTER_PARTY_TIMEOUT = "counter_party_timeout"
    POST_REFUND = "post_refund"
    POST_CLAIM = "post_claim"


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
    def opportunities(self) -> list:
        """Get the opportunities."""
        return self.db.get("opportunities", ["opportunity"])

    @property
    def quotes(self) -> list:
        """Get the quotes."""
        return self.db.get("quotes", ["quote"])

    @property
    def counter_party_timeout(self) -> bool:
        """Check if counter party timeout was hit."""
        return self.db.get("counter_party_timeout", False)

    @property
    def tx_state(self) -> TxState:
        """Get the transaction state."""
        return self.db.get("tx_state")


class AwaitingOpportunityRound(CollectSameUntilThresholdRound):
    """AwaitingOpportunityRound"""

    payload_class = AwaitingOpportunityPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if self.synchronized_data.opportunities:
            return self.synchronized_data, Event.TRIGGERED

        return self.synchronized_data, Event.NOT_TRIGGERED


class SubmitRFQRound(CollectSameUntilThresholdRound):
    """SubmitRFQRound"""

    payload_class = SubmitRFQPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        return self.synchronized_data, Event.DONE


class AwaitQuotesRound(CollectSameUntilThresholdRound):
    """AwaitQuotesRound"""

    payload_class = AwaitQuotesPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if not self.synchronized_data.quotes:
            return self.synchronized_data, Event.NO_QUOTES

        return self.synchronized_data, Event.QUOTES


class SelectQuotesRound(CollectSameUntilThresholdRound):
    """SelectQuotesRound"""

    payload_class = SelectQuotesPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        return self.synchronized_data, Event.ACCEPT_QUOTES


class PrepareNewSwapTransactionsRound(CollectSameUntilThresholdRound):
    """PrepareNewSwapTransactionsRound"""

    payload_class = PrepareNewSwapTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        return self.synchronized_data, Event.DONE
        # return self.synchronized_data, Event.FINALISED


class AwaitSupplierTransactionsRound(CollectSameUntilThresholdRound):
    """AwaitSupplierTransactionsRound"""

    payload_class = AwaitSupplierTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if self.synchronized_data.counter_party_timeout:
            self.synchronized_data, Event.COUNTER_PARTY_TIMEOUT

        return self.synchronized_data, Event.DONE


class PrepareClaimTransactionsRound(CollectSameUntilThresholdRound):
    """PrepareClaimTransactionsRound"""

    payload_class = PrepareClaimTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if self.synchronized_data.tx_state == TxState.POST_CLAIM:
            # self.tx_state = TxState.PRE_TRANSACTION
            return self.synchronized_data, Event.FINALISED

        self.tx_state = TxState.POST_CLAIM
        return self.synchronized_data, Event.DONE


class PrepareRefundTransactionsRound(CollectSameUntilThresholdRound):
    """PrepareRefundTransactionsRound"""

    payload_class = PrepareRefundTransactionsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""

        if self.synchronized_data.tx_state == TxState.POST_REFUND:
            # self.tx_state = TxState.PRE_TRANSACTION
            return self.synchronized_data, Event.FINALISED

        return self.synchronized_data, Event.DONE


class PostTransactionRound(CollectSameUntilThresholdRound):
    """PostTransactionRound"""

    payload_class = PostTransactionPayload
    payload_attribute = ""  # TODO: update
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


class FinalisedSwapTransactionsRound(DegenerateRound):
    """FinalisedSwapTransactionsRound"""


class NoOpportunityRound(DegenerateRound):
    """NoOpportunityRound"""


class SuccessfulExecutionRound(DegenerateRound):
    """SuccessfulExecutionRound"""


class UnSuccessfulExecutionRound(DegenerateRound):
    """UnSuccessfulExecutionRound"""


class QSSolverAbciApp(AbciApp[Event]):
    """QSSolverAbciApp"""

    initial_round_cls: AppState = PostTransactionRound
    initial_states: Set[AppState] = {AwaitingOpportunityRound, PostTransactionRound}
    transition_function: AbciAppTransitionFunction = {
        AwaitQuotesRound: {
            Event.NO_QUOTES: NoOpportunityRound,
            Event.QUOTES: SelectQuotesRound
        },
        AwaitSupplierTransactionsRound: {
            Event.COUNTER_PARTY_TIMEOUT: PrepareRefundTransactionsRound,
            Event.DONE: PrepareClaimTransactionsRound
        },
        AwaitingOpportunityRound: {
            Event.NOT_TRIGGERED: NoOpportunityRound,
            Event.TRIGGERED: SubmitRFQRound
        },
        PostTransactionRound: {
            Event.POST_CLAIM: SuccessfulExecutionRound,
            Event.POST_NEW_SWAP: AwaitSupplierTransactionsRound,
            Event.POST_REFUND: UnSuccessfulExecutionRound
        },
        PrepareClaimTransactionsRound: {
            Event.DONE: FinalisedClaimTransactionsRound,
            Event.FINALISED: SuccessfulExecutionRound
        },
        PrepareNewSwapTransactionsRound: {
            Event.DONE: FinalisedSwapTransactionsRound,
            Event.FINALISED: AwaitSupplierTransactionsRound
        },
        PrepareRefundTransactionsRound: {
            Event.DONE: FinalisedRefundTransactionsRound,
            Event.FINALISED: UnSuccessfulExecutionRound
        },
        SelectQuotesRound: {
            Event.ACCEPT_QUOTES: PrepareNewSwapTransactionsRound
        },
        SubmitRFQRound: {
            Event.DONE: AwaitQuotesRound
        },
        SuccessfulExecutionRound: {},
        FinalisedClaimTransactionsRound: {},
        UnSuccessfulExecutionRound: {},
        NoOpportunityRound: {},
        FinalisedRefundTransactionsRound: {},
        FinalisedSwapTransactionsRound: {}
    }
    final_states: Set[AppState] = {FinalisedClaimTransactionsRound, UnSuccessfulExecutionRound, NoOpportunityRound, FinalisedRefundTransactionsRound, FinalisedSwapTransactionsRound, SuccessfulExecutionRound}
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        AwaitingOpportunityRound: {"participants"},
		PostTransactionRound: {"participants"},
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        FinalisedClaimTransactionsRound: {'most_voted_tx_hash'},
		UnSuccessfulExecutionRound: set(),
		NoOpportunityRound: set(),
		FinalisedRefundTransactionsRound: {'most_voted_tx_hash'},
		FinalisedSwapTransactionsRound: {'most_voted_tx_hash'},
		SuccessfulExecutionRound: {'most_voted_tx_hash'},
    }
