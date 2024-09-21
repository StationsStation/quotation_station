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

"""This package contains the rounds of QSOrchestratorAbciApp."""

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

from packages.eightballer.skills.qs_orchestrator_abci.payloads import (
    CreateContainersPayload,
    HealthCheckPayload,
)


class Event(Enum):
    """QSOrchestratorAbciApp Events"""

    DONE = "done"
    UNHEALTHY = "unhealthy"
    HEALTHY = "healthy"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class CreateContainersRound(CollectSameUntilThresholdRound):
    """CreateContainersRound"""

    payload_class = CreateContainersPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: CreateContainersPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CreateContainersPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class HealthCheckRound(CollectSameUntilThresholdRound):
    """HealthCheckRound"""

    payload_class = HealthCheckPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: HealthCheckPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: HealthCheckPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class SuccessfulDeploymentRound(DegenerateRound):
    """SuccessfulDeploymentRound"""


class QSOrchestratorAbciApp(AbciApp[Event]):
    """QSOrchestratorAbciApp"""

    initial_round_cls: AppState = HealthCheckRound
    initial_states: Set[AppState] = {HealthCheckRound}
    transition_function: AbciAppTransitionFunction = {
        CreateContainersRound: {
            Event.DONE: HealthCheckRound
        },
        HealthCheckRound: {
            Event.HEALTHY: SuccessfulDeploymentRound,
            Event.UNHEALTHY: CreateContainersRound
        },
        SuccessfulDeploymentRound: {}
    }
    final_states: Set[AppState] = {SuccessfulDeploymentRound}
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        HealthCheckRound: {"participants"},
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        SuccessfulDeploymentRound: set(),
    }
