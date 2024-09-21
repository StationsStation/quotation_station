# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
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

"""This module contains the scaffold contract definition."""

from typing import Any

from aea.common import JSONLike
from packages.eightballer.contracts.cross_chain_atomic_swap import PUBLIC_ID
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi, Address


class CrossChainAtomicSwap(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PUBLIC_ID

    @classmethod
    def get_raw_transaction(
        cls, ledger_api: LedgerApi, contract_address: str, **kwargs: Any
    ) -> JSONLike:
        """
        Handler method for the 'GET_RAW_TRANSACTION' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        :param ledger_api: the ledger apis.
        :param contract_address: the contract address.
        :param kwargs: the keyword arguments.
        :return: the tx  # noqa: DAR202
        """
        raise NotImplementedError

    @classmethod
    def get_raw_message(
        cls, ledger_api: LedgerApi, contract_address: str, **kwargs: Any
    ) -> bytes:
        """
        Handler method for the 'GET_RAW_MESSAGE' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        :param ledger_api: the ledger apis.
        :param contract_address: the contract address.
        :param kwargs: the keyword arguments.
        :return: the tx  # noqa: DAR202
        """
        raise NotImplementedError

    @classmethod
    def get_state(
        cls, ledger_api: LedgerApi, contract_address: str, **kwargs: Any
    ) -> JSONLike:
        """
        Handler method for the 'GET_STATE' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        :param ledger_api: the ledger apis.
        :param contract_address: the contract address.
        :param kwargs: the keyword arguments.
        :return: the tx  # noqa: DAR202
        """
        raise NotImplementedError

    @classmethod
    def domain_separator(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'domain_separator' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.DOMAIN_SEPARATOR().call()
        return {
            'str': result
        }



    @classmethod
    def eth_token_address(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'eth_token_address' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.ETH_TOKEN_ADDRESS().call()
        return {
            'address': result
        }



    @classmethod
    def magic_m(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'magic_m' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.MAGIC_M().call()
        return {
            'int': result
        }



    @classmethod
    def magic_n(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'magic_n' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.MAGIC_N().call()
        return {
            'int': result
        }



    @classmethod
    def version(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'version' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.VERSION().call()
        return {
            'str': result
        }



    @classmethod
    def get_msg_hash(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        buyer: Address,
        swapId: int,
        secret: str,
        deadline: int
        ) -> JSONLike:
        """Handler method for the 'get_msg_hash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getMsgHash(buyer=buyer,
        swapId=swapId,
        secret=secret,
        deadline=deadline).call()
        return {
            'str': result
        }



    @classmethod
    def max_timelock(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'max_timelock' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.maxTimelock().call()
        return {
            'int': result
        }



    @classmethod
    def min_timelock(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'min_timelock' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.minTimelock().call()
        return {
            'int': result
        }



    @classmethod
    def nonce(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'nonce' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.nonce().call()
        return {
            'int': result
        }



    @classmethod
    def swaps(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        var_0: int
        ) -> JSONLike:
        """Handler method for the 'swaps' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.swaps(var_0).call()
        return {
            'seller': result,
        'buyer': result,
        'token': result,
        'amount': result,
        'secretHash': result,
        'expirationClaim': result,
        'expirationTotal': result,
        'status': result,
        'secret': result
        }


    @classmethod
    def claim(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        swapId: int,
        secret: str
        ) -> JSONLike:
        """Handler method for the 'claim' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        tx = instance.functions.claim(swapId=swapId,
        secret=secret)
        return tx


    @classmethod
    def claim_relay(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        swapId: int,
        secret: str,
        deadline: int,
        v: int,
        r: str,
        s: str
        ) -> JSONLike:
        """Handler method for the 'claim_relay' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        tx = instance.functions.claimRelay(swapId=swapId,
        secret=secret,
        deadline=deadline,
        v=v,
        r=r,
        s=s)
        return tx


    @classmethod
    def new_swap(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        buyer: Address,
        secretHash: str,
        expiration: int,
        token: Address,
        amount: int,
        swapSide: bool
        ) -> JSONLike:
        """Handler method for the 'new_swap' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        tx = instance.functions.newSwap(buyer=buyer,
        secretHash=secretHash,
        expiration=expiration,
        token=token,
        amount=amount,
        swapSide=swapSide)
        return tx


    @classmethod
    def refund(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        swapId: int
        ) -> JSONLike:
        """Handler method for the 'refund' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        tx = instance.functions.refund(swapId=swapId)
        return tx
