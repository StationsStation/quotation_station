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

"""This package contains round behaviours of QSSolverAbciApp."""

from abc import ABC
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.eightballer.skills.qs_solver_abci.models import Params
from packages.eightballer.skills.qs_solver_abci.rounds import (
    SynchronizedData,
    QSSolverAbciApp,
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
from packages.eightballer.skills.qs_solver_abci.rounds import (
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


class QSSolverBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the qs_solver_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class AwaitQuotesBehaviour(QSSolverBaseBehaviour):
    """AwaitQuotesBehaviour"""

    matching_round: Type[AbstractRound] = AwaitQuotesRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = AwaitQuotesPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class AwaitSupplierTransactionsBehaviour(QSSolverBaseBehaviour):
    """AwaitSupplierTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = AwaitSupplierTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = AwaitSupplierTransactionsPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class AwaitingOpportunityBehaviour(QSSolverBaseBehaviour):
    """AwaitingOpportunityBehaviour"""

    matching_round: Type[AbstractRound] = AwaitingOpportunityRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = AwaitingOpportunityPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PostTransactionBehaviour(QSSolverBaseBehaviour):
    """PostTransactionBehaviour"""

    matching_round: Type[AbstractRound] = PostTransactionRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PostTransactionPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareClaimTransactionsBehaviour(QSSolverBaseBehaviour):
    """PrepareClaimTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = PrepareClaimTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareClaimTransactionsPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareNewSwapTransactionsBehaviour(QSSolverBaseBehaviour):
    """PrepareNewSwapTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = PrepareNewSwapTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareNewSwapTransactionsPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareRefundTransactionsBehaviour(QSSolverBaseBehaviour):
    """PrepareRefundTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = PrepareRefundTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareRefundTransactionsPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SelectQuotesBehaviour(QSSolverBaseBehaviour):
    """SelectQuotesBehaviour"""

    matching_round: Type[AbstractRound] = SelectQuotesRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SelectQuotesPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SubmitRFQBehaviour(QSSolverBaseBehaviour):
    """SubmitRFQBehaviour"""

    matching_round: Type[AbstractRound] = SubmitRFQRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SubmitRFQPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class QSSolverRoundBehaviour(AbstractRoundBehaviour):
    """QSSolverRoundBehaviour"""

    initial_behaviour_cls = PostTransactionBehaviour
    abci_app_cls = QSSolverAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        AwaitQuotesBehaviour,
        AwaitSupplierTransactionsBehaviour,
        AwaitingOpportunityBehaviour,
        PostTransactionBehaviour,
        PrepareClaimTransactionsBehaviour,
        PrepareNewSwapTransactionsBehaviour,
        PrepareRefundTransactionsBehaviour,
        SelectQuotesBehaviour,
        SubmitRFQBehaviour
    ]
