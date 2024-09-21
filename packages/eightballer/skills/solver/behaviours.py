
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

"""This package contains the Solver composite behaviour."""

from typing import Set, Type

from packages.eightballer.skills.ui_loader_abci.behaviours import ComponentLoadingRoundBehaviour
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.registration_abci.behaviours import (
    AgentRegistrationRoundBehaviour,
    RegistrationStartupBehaviour,
)
from packages.valory.skills.reset_pause_abci.behaviours import (
    ResetPauseABCIConsensusBehaviour,
)
from packages.valory.skills.transaction_settlement_abci.behaviours import (
    TransactionSettlementRoundBehaviour,
)
from packages.eightballer.skills.qs_solver_abci.behaviours import (
    QSSolverRoundBehaviour,
)
from packages.eightballer.skills.solver.composition import CompositeAbciApp


class SolverConsensusBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages for the Solver."""

    initial_behaviour_cls = RegistrationStartupBehaviour
    abci_app_cls = CompositeAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = {
        *AgentRegistrationRoundBehaviour.behaviours,
        *ComponentLoadingRoundBehaviour.behaviours,
        *QSSolverRoundBehaviour.behaviours,
        *TransactionSettlementRoundBehaviour.behaviours,
        *ResetPauseABCIConsensusBehaviour.behaviours,
    }