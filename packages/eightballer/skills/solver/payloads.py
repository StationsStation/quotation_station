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

"""This module contains the transaction payloads of the QSSolverAbciApp."""

from dataclasses import dataclass

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


@dataclass(frozen=True)
class AwaitQuotesPayload(BaseTxPayload):
    """Represent a transaction payload for the AwaitQuotesRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class AwaitSupplierTransactionsPayload(BaseTxPayload):
    """Represent a transaction payload for the AwaitSupplierTransactionsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class AwaitingOpportunityPayload(BaseTxPayload):
    """Represent a transaction payload for the AwaitingOpportunityRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class PostTransactionPayload(BaseTxPayload):
    """Represent a transaction payload for the PostTransactionRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class PrepareClaimTransactionsPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareClaimTransactionsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class PrepareNewSwapTransactionsPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareNewSwapTransactionsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class PrepareRefundTransactionsPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareRefundTransactionsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class SelectQuotesPayload(BaseTxPayload):
    """Represent a transaction payload for the SelectQuotesRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class SubmitRFQPayload(BaseTxPayload):
    """Represent a transaction payload for the SubmitRFQRound."""

    # TODO: define your attributes

