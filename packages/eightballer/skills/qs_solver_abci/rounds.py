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
    AbstractRound,
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


class Event(Enum):
    """QSSolverAbciApp Events"""

    DONE = "done"
    POST_REFUND = "post_refund"
    QUOTES = "quotes"
    FINALISED = "finalised"
    TRIGGERED = "triggered"
    ACCEPT_QUOTES = "accept_quotes"
    NOT_TRIGGERED = "not_triggered"
    NO_QUOTES = "no_quotes"
    POST_CLAIM = "post_claim"
    POST_NEW_SWAP = "post_new_swap"
    COUNTER_PARTY_TIMEOUT = "counter_party_timeout"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class AwaitQuotesRound(AbstractRound):
    """AwaitQuotesRound"""

    payload_class = AwaitQuotesPayload
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

    def check_payload(self, payload: AwaitQuotesPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AwaitQuotesPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class AwaitSupplierTransactionsRound(AbstractRound):
    """AwaitSupplierTransactionsRound"""

    payload_class = AwaitSupplierTransactionsPayload
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

    def check_payload(self, payload: AwaitSupplierTransactionsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AwaitSupplierTransactionsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class AwaitingOpportunityRound(AbstractRound):
    """AwaitingOpportunityRound"""

    payload_class = AwaitingOpportunityPayload
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

    def check_payload(self, payload: AwaitingOpportunityPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AwaitingOpportunityPayload) -> None:
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


class PrepareNewSwapTransactionsRound(AbstractRound):
    """PrepareNewSwapTransactionsRound"""

    payload_class = PrepareNewSwapTransactionsPayload
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

    def check_payload(self, payload: PrepareNewSwapTransactionsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareNewSwapTransactionsPayload) -> None:
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


class SelectQuotesRound(AbstractRound):
    """SelectQuotesRound"""

    payload_class = SelectQuotesPayload
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

    def check_payload(self, payload: SelectQuotesPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: SelectQuotesPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class SubmitRFQRound(AbstractRound):
    """SubmitRFQRound"""

    payload_class = SubmitRFQPayload
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

    def check_payload(self, payload: SubmitRFQPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: SubmitRFQPayload) -> None:
        """Process payload."""
        raise NotImplementedError


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
    initial_states: Set[AppState] = {PostTransactionRound, AwaitingOpportunityRound}
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
        UnSuccessfulExecutionRound: {},
        FinalisedClaimTransactionsRound: {},
        FinalisedSwapTransactionsRound: {},
        NoOpportunityRound: {},
        FinalisedRefundTransactionsRound: {}
    }
    final_states: Set[AppState] = {SuccessfulExecutionRound, UnSuccessfulExecutionRound, FinalisedClaimTransactionsRound, NoOpportunityRound, FinalisedRefundTransactionsRound, FinalisedSwapTransactionsRound}
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        PostTransactionRound: [],
    	AwaitingOpportunityRound: [],
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        SuccessfulExecutionRound: [],
    	UnSuccessfulExecutionRound: [],
    	FinalisedClaimTransactionsRound: [],
    	NoOpportunityRound: [],
    	FinalisedRefundTransactionsRound: [],
    	FinalisedSwapTransactionsRound: [],
    }
