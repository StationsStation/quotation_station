
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

"""This module contains the Composite ABCI application."""

from packages.valory.skills.abstract_round_abci.abci_app_chain import (
    AbciAppTransitionMapping,
    chain,
)
from packages.valory.skills.registration_abci.rounds import (
    AgentRegistrationAbciApp,
    FinishedRegistrationRound,
    RegistrationRound,
)
from packages.valory.skills.reset_pause_abci.rounds import (
    FinishedResetAndPauseErrorRound,
    FinishedResetAndPauseRound,
    ResetAndPauseRound,
    ResetPauseAbciApp,
)
from packages.valory.skills.transaction_settlement_abci.rounds import (
    FailedRound,
    FinishedTransactionSubmissionRound,
    RandomnessTransactionSubmissionRound,
    TransactionSubmissionAbciApp,
)
from packages.eightballer.skills.qs_executor_abci.rounds import (
    FinalisedRefundTransactionsRound,
    SuccessfulExecutionRound,
    FinalisedClaimTransactionsRound,
    FinalisedSupplyTransactionsRound,
    UnSuccessfulExecutionRound,
    QSExecutorAbciApp,
    PostTransactionRound,
    CollectExchangeDataRound,
)

abci_app_transition_mapping: AbciAppTransitionMapping = {
    FinishedRegistrationRound: CollectExchangeDataRound,
    SuccessfulExecutionRound: ResetAndPauseRound,
    FinalisedSupplyTransactionsRound: RandomnessTransactionSubmissionRound,
    FinalisedClaimTransactionsRound: RandomnessTransactionSubmissionRound,
    FinalisedRefundTransactionsRound: RandomnessTransactionSubmissionRound,
    UnSuccessfulExecutionRound: ResetAndPauseRound,
    FinishedTransactionSubmissionRound: PostTransactionRound,
    FinishedResetAndPauseRound: CollectExchangeDataRound,
    FinishedResetAndPauseErrorRound: RegistrationRound,
}

CompositeAbciApp = chain(
    (
        AgentRegistrationAbciApp,
        QSExecutorAbciApp,
        TransactionSubmissionAbciApp,
        ResetPauseAbciApp,
    ),
    abci_app_transition_mapping,
)
