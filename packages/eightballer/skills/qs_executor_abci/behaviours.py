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

"""This package contains round behaviours of QSExecutorAbciApp."""

from abc import ABC
import json
from typing import Generator, Set, Type, cast

from packages.eightballer.protocols.balances.message import BalancesMessage
from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.eightballer.skills.qs_executor_abci.models import Params
from packages.eightballer.skills.qs_executor_abci.rounds import (
    SynchronizedData,
    QSExecutorAbciApp,
    AwaitBuyerTransactionsRound,
    AwaitRFQsRound,
    CollectExchangeDataRound,
    PostTransactionRound,
    PrepareClaimTransactionsRound,
    PrepareRefundTransactionsRound,
    PrepareSupplyTransactionRound,
)
from packages.eightballer.skills.qs_executor_abci.rounds import (
    AwaitBuyerTransactionsPayload,
    AwaitRFQsPayload,
    CollectExchangeDataPayload,
    PostTransactionPayload,
    PrepareClaimTransactionsPayload,
    PrepareRefundTransactionsPayload,
    PrepareSupplyTransactionPayload,
)


class QSExecutorBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the qs_executor_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class AwaitBuyerTransactionsBehaviour(QSExecutorBaseBehaviour):
    """AwaitBuyerTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = AwaitBuyerTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = AwaitBuyerTransactionsPayload(sender=sender, content="dummy_content")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class AwaitRFQsBehaviour(QSExecutorBaseBehaviour):
    """AwaitRFQsBehaviour"""

    matching_round: Type[AbstractRound] = AwaitRFQsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = AwaitRFQsPayload(sender=sender, content="dummy_content")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CollectExchangeDataBehaviour(QSExecutorBaseBehaviour):
    """CollectExchangeDataBehaviour"""

    matching_round: Type[AbstractRound] = CollectExchangeDataRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        dex_exchange_ids = self.params.dex_data_retrieval_config.exchange_ids
        dex_extra_kwargs = self.params.dex_data_retrieval_config.extra_kwargs

        cex_exchange_ids = self.params.cex_data_retrieval_config.exchange_ids
        cex_extra_kwargs = self.params.cex_data_retrieval_config.extra_kwargs

        exchange_to_balances = {}
        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            for exchange_id in dex_exchange_ids:
                params = {}
                if dex_extra_kwargs is not None:
                    params = dex_extra_kwargs.get(exchange_id, {}).copy()
                # extra kwargs must in the form str to bytes
                for key, value in params.items():
                    params[key] = value.encode("utf-8")

                msg: BalancesMessage = yield from self.get_dcxt_response(
                    protocol_performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                    exchange_id=exchange_id,
                    params=params,
                )

                balances = self._from_balances_to_dict(msg, exchange_id)
                self.context.logger.info(f"Received {len(balances[exchange_id])} balances from {exchange_id}")
                exchange_to_balances.update(balances)

            for exchange_id in cex_exchange_ids:
                params = {}
                if cex_extra_kwargs is not None:
                    params = cex_extra_kwargs.get(exchange_id, {}).copy()
                # extra kwargs must in the form str to bytes
                for key, value in params.items():
                    params[key] = value.encode("utf-8")

                msg: BalancesMessage = yield from self.get_ccxt_response(
                    protocol_performative=BalancesMessage.Performative.GET_ALL_BALANCES,
                    exchange_id=exchange_id,
                    params=params,
                )

                balances = self._from_balances_to_dict(msg, exchange_id)
                self.context.logger.info(f"Received {len(balances[exchange_id])} balances from {exchange_id}")
                exchange_to_balances.update(balances)

        
            sender = self.context.agent_address
            payload = CollectExchangeDataPayload(
                sender=sender,
                content=json.dumps(exchange_to_balances),
            )
        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _from_balances_to_dict(self, balances_msg: BalancesMessage, exchange_id: str) -> dict:
        """Convert balances message to dict."""
        return {
            exchange_id: [b.as_json() for b in balances_msg.balances.balances],
        }


class PostTransactionBehaviour(QSExecutorBaseBehaviour):
    """PostTransactionBehaviour"""

    matching_round: Type[AbstractRound] = PostTransactionRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PostTransactionPayload(sender=sender, content="dummy_content")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareClaimTransactionsBehaviour(QSExecutorBaseBehaviour):
    """PrepareClaimTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = PrepareClaimTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareClaimTransactionsPayload(sender=sender, content="dummy_content")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareRefundTransactionsBehaviour(QSExecutorBaseBehaviour):
    """PrepareRefundTransactionsBehaviour"""

    matching_round: Type[AbstractRound] = PrepareRefundTransactionsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareRefundTransactionsPayload(sender=sender, content="dummy_content")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareSupplyTransactionBehaviour(QSExecutorBaseBehaviour):
    """PrepareSupplyTransactionBehaviour"""

    matching_round: Type[AbstractRound] = PrepareSupplyTransactionRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareSupplyTransactionPayload(sender=sender, content="dummy_content")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class QSExecutorRoundBehaviour(AbstractRoundBehaviour):
    """QSExecutorRoundBehaviour"""

    initial_behaviour_cls = PostTransactionBehaviour
    abci_app_cls = QSExecutorAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        AwaitBuyerTransactionsBehaviour,
        AwaitRFQsBehaviour,
        CollectExchangeDataBehaviour,
        PostTransactionBehaviour,
        PrepareClaimTransactionsBehaviour,
        PrepareRefundTransactionsBehaviour,
        PrepareSupplyTransactionBehaviour
    ]
