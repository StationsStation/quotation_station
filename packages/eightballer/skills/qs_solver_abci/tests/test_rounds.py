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

"""This package contains the tests for rounds of QSSolver."""

from typing import Any, Type, Dict, List, Callable, Hashable, Mapping
from dataclasses import dataclass, field

import pytest

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
from packages.eightballer.skills.qs_solver_abci.rounds import (
    AbstractRound,
    Event,
    SynchronizedData,
    AwaitQuotesRound,
    AwaitSupplierTransactionsRound,
    AwaitingOpportunityRound,
    PostTransactionRound,
    PrepareClaimTransactionsRound,
    PrepareNewSwapTransactionsRound,
    PrepareRefundTransactionsRound,
    SelectQuotesRound,
    SubmitRFQRound,
)
from packages.valory.skills.abstract_round_abci.base import (
    BaseTxPayload,
)
from packages.valory.skills.abstract_round_abci.test_tools.rounds import (
    BaseRoundTestClass,
    BaseOnlyKeeperSendsRoundTest,
    BaseCollectDifferentUntilThresholdRoundTest,
    BaseCollectSameUntilThresholdRoundTest,
 )


@dataclass
class RoundTestCase:
    """RoundTestCase"""

    name: str
    initial_data: Dict[str, Hashable]
    payloads: Mapping[str, BaseTxPayload]
    final_data: Dict[str, Hashable]
    event: Event
    synchronized_data_attr_checks: List[Callable] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)


MAX_PARTICIPANTS: int = 4


class BaseQSSolverRoundTest(BaseRoundTestClass):
    """Base test class for QSSolver rounds."""

    round_cls: Type[AbstractRound]
    synchronized_data: SynchronizedData
    _synchronized_data_class = SynchronizedData
    _event_class = Event

    def run_test(self, test_case: RoundTestCase) -> None:
        """Run the test"""

        self.synchronized_data.update(**test_case.initial_data)

        test_round = self.round_cls(
            synchronized_data=self.synchronized_data,
        )

        self._complete_run(
            self._test_round(
                test_round=test_round,
                round_payloads=test_case.payloads,
                synchronized_data_update_fn=lambda sync_data, _: sync_data.update(**test_case.final_data),
                synchronized_data_attr_checks=test_case.synchronized_data_attr_checks,
                exit_event=test_case.event,
                **test_case.kwargs,  # varies per BaseRoundTestClass child
            )
        )


class TestAwaitQuotesRound(BaseQSSolverRoundTest):
    """Tests for AwaitQuotesRound."""

    round_class = AwaitQuotesRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestAwaitSupplierTransactionsRound(BaseQSSolverRoundTest):
    """Tests for AwaitSupplierTransactionsRound."""

    round_class = AwaitSupplierTransactionsRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestAwaitingOpportunityRound(BaseQSSolverRoundTest):
    """Tests for AwaitingOpportunityRound."""

    round_class = AwaitingOpportunityRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPostTransactionRound(BaseQSSolverRoundTest):
    """Tests for PostTransactionRound."""

    round_class = PostTransactionRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPrepareClaimTransactionsRound(BaseQSSolverRoundTest):
    """Tests for PrepareClaimTransactionsRound."""

    round_class = PrepareClaimTransactionsRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPrepareNewSwapTransactionsRound(BaseQSSolverRoundTest):
    """Tests for PrepareNewSwapTransactionsRound."""

    round_class = PrepareNewSwapTransactionsRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPrepareRefundTransactionsRound(BaseQSSolverRoundTest):
    """Tests for PrepareRefundTransactionsRound."""

    round_class = PrepareRefundTransactionsRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestSelectQuotesRound(BaseQSSolverRoundTest):
    """Tests for SelectQuotesRound."""

    round_class = SelectQuotesRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestSubmitRFQRound(BaseQSSolverRoundTest):
    """Tests for SubmitRFQRound."""

    round_class = SubmitRFQRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)

