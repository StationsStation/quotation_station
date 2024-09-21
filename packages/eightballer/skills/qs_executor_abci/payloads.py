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

"""This module contains the transaction payloads of the QSExecutorAbciApp."""

from dataclasses import dataclass

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


@dataclass(frozen=True)
class AwaitBuyerTransactionsPayload(BaseTxPayload):
    """Represent a transaction payload for the AwaitBuyerTransactionsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class AwaitRFQsPayload(BaseTxPayload):
    """Represent a transaction payload for the AwaitRFQsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class CollectExchangeDataPayload(BaseTxPayload):
    """Represent a transaction payload for the CollectExchangeDataRound."""

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
class PrepareRefundTransactionsPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareRefundTransactionsRound."""

    # TODO: define your attributes


@dataclass(frozen=True)
class PrepareSupplyTransactionPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareSupplyTransactionRound."""

    # TODO: define your attributes

