# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 zarathustra
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

"""This module contains the shared state for the abci skill of CompositeAbciApp."""

from enum import StrEnum

from packages.valory.skills.abstract_round_abci.models import ApiSpecs, BaseParams
from packages.valory.skills.abstract_round_abci.models import (
    BenchmarkTool as BaseBenchmarkTool,
)
from packages.valory.skills.abstract_round_abci.models import Requests as BaseRequests
from packages.valory.skills.abstract_round_abci.models import (
    SharedState as BaseSharedState,
)
from packages.eightballer.skills.solver.composition import CompositeAbciApp


class ExecutionMode(StrEnum):
    EOA = "EOA"
    MULTISIG = "MULTI"


class SharedState(BaseSharedState):
    """Keep the current shared state of the composite skill."""

    abci_app_cls = CompositeAbciApp


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
