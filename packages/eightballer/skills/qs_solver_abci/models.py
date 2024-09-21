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

"""This module contains the shared state for the abci skill of QSSolverAbciApp."""

from enum import Enum

from packages.valory.skills.abstract_round_abci.models import ApiSpecs, BaseParams
from packages.valory.skills.abstract_round_abci.models import (
    BenchmarkTool as BaseBenchmarkTool,
)
from packages.valory.skills.abstract_round_abci.models import Requests as BaseRequests
from packages.valory.skills.abstract_round_abci.models import (
    SharedState as BaseSharedState,
)
from packages.eightballer.skills.qs_solver_abci.rounds import QSSolverAbciApp


class ExecutionMode(Enum):
    EOA = "EOA"
    MULTISIG = "MULTI"


class SharedState(BaseSharedState):
    """Keep the current shared state of the skill."""

    abci_app_cls = QSSolverAbciApp


class RandomnessApi(ApiSpecs):
    """A model for randomness api specifications."""


class Params(BaseParams):

    def __init__(self, *args, **kwargs):
        executor_setup = kwargs["executor_setup"]
        self.executor_mode: ExecutionMode = ExecutionMode[executor_setup["execution_mode"]]
        self.quotable_margin_percent: float = executor_setup["quotable_margin_percent"]

        super().__init__(*args, **kwargs)


Requests = BaseRequests
BenchmarkTool = BaseBenchmarkTool
