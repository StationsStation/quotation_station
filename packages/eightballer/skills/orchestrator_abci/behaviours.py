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

"""This package contains round behaviours of OrchestratorAbciApp."""

from abc import ABC
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.eightballer.skills.orchestrator_abci.models import Params
from packages.eightballer.skills.orchestrator_abci.rounds import (
    SynchronizedData,
    OrchestratorAbciApp,
    CreateContainersRound,
    HealthCheckRound,
)
from packages.eightballer.skills.orchestrator_abci.rounds import (
    CreateContainersPayload,
    HealthCheckPayload,
)


class OrchestratorBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the orchestrator_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class CreateContainersBehaviour(OrchestratorBaseBehaviour):
    """CreateContainersBehaviour"""

    matching_round: Type[AbstractRound] = CreateContainersRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CreateContainersPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class HealthCheckBehaviour(OrchestratorBaseBehaviour):
    """HealthCheckBehaviour"""

    matching_round: Type[AbstractRound] = HealthCheckRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = HealthCheckPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class OrchestratorRoundBehaviour(AbstractRoundBehaviour):
    """OrchestratorRoundBehaviour"""

    initial_behaviour_cls = HealthCheckBehaviour
    abci_app_cls = OrchestratorAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        CreateContainersBehaviour,
        HealthCheckBehaviour
    ]
