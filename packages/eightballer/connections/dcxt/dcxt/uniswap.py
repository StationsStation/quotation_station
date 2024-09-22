"""
Balancer exchange.
"""
from decimal import Decimal
import json
from glob import glob
from pathlib import Path
import time

from aea_ledger_ethereum import Account, ContractLogicError

from packages.eightballer.connections.dcxt.dcxt.exceptions import ConfigurationError, SorRetrievalException
from packages.eightballer.protocols.balances.custom_types import Balance, Balances
from packages.eightballer.protocols.markets.custom_types import Market, Markets
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue
from packages.eightballer.protocols.positions.message import PositionsMessage

GAS_PRICE_PREMIUM = 20
GAS_SPEED = "fast"
GAS_PRICE = 888


DEFAULT_ENCODING = "utf-8"

PACKAGE_DIR = Path(__file__).parent
ABI_DIR = PACKAGE_DIR / "abis"

ABI_MAPPING = {
    Path(path)
    .stem.upper(): open(path, encoding=DEFAULT_ENCODING)  # pylint: disable=R1732
    .read()  # pylint: disable=R1732
    for path in glob(str(ABI_DIR / "*.json"))
}

ETH_KEYPATH = 'ethereum_private_key.txt'

BASE_ASSET_ID = '0x6b175474e89094c44da98b954eedeac495271d0f'


class UniswapClient:
    """
    Balancer exchange.
    """

    def __init__(self, *args, **kwargs):  # pylint: disable=super-init-not-called
        del args
        custom_kwargs = kwargs.get("kwargs", {})
        self.chain_name = custom_kwargs.get("chain_id")
        if not self.chain_name:
            raise ConfigurationError("Chain name not provided to BalancerClient")

        self.rpc_url = custom_kwargs.get("rpc_url")
        if not self.rpc_url:
            raise ConfigurationError("RPC URL not provided to BalancerClient")

        self.etherscan_api_key = custom_kwargs.get("etherscan_api_key")
        if not self.etherscan_api_key:
            raise ConfigurationError("Etherscan API key not provided to BalancerClient")

        self.account = Account.from_key(  # pylint: disable=E1120
            private_key=kwargs.get('auth').get("private_key").strip()
        )  # pylint: disable=E1120
        self.bal = balpy.balpy(
            self.chain_name,
            manualEnv={
                "privateKey": self.account._private_key,
                "customRPC": self.rpc_url,
                "etherscanApiKey": self.etherscan_api_key,
            },
        )

        self.gas_price = kwargs.get("gas_price", None)
        self.gas_price_premium = kwargs.get("gas_price_premium", GAS_PRICE_PREMIUM)

    async def fetch_markets(
        self,
        params: dict,
    ):
        """
        Fetches the markets.

        :return: The markets.
        """
        del params
        try:
            markets = [
                {
                    'id': pool_id,
                    'symbol': 'OLAS/USDC',
                    'base': 'OLAS',
                    'quote': 'USDC',
                    'spot': True,
                }
                for pool_id in self.pool_ids
            ]
            return Markets(
                markets=[Market(**market) for market in markets],
            )
        except SorRetrievalException as exc:
            raise SorRetrievalException(
                f'Error fetching markets from chainId {self.chain_name} Balancer: {exc}'
            ) from exc

    async def fetch_balances(self, *args, **kwargs):
        """
        Fetches the balances.

        :return: The balances.
        """
        del args, kwargs
        balances = Balances(
            balances=[
                Balance(
                    asset_id=BASE_ASSET_ID,
                    free=0,
                    used=0,
                    total=0,
                )
            ]
        )
        return balances

    @property
    def pool_ids(self):
        """
        Get the pool IDs.

        :return: The pool IDs.
        """
        # We read in the pool IDs from a file for now.
        with open(Path(__file__).parent / 'data' / 'balancer' / "mainnet.json", "r", encoding=DEFAULT_ENCODING) as file:
            json_data = json.loads(file.read())['pools']
        if 'Element' in json_data:
            del json_data['Element']
        return json_data

    async def fetch_tickers(self, *args, **kwargs):
        """
        Fetches the tickers.

        :return: The tickers.
        """

        # We temporarily assume that the tickers are the same as the markets, and use the pool IDs to get the tickers.

        await self.fetch_markets(*args, **kwargs)

        params = (
            self.pool_ids
        )  # however as we are not able to collect for *all* ppols, we just select a few to get the data for.

        # We use olas USDC as the base pair for now.

        OLAS_ADDRESS = '0x0001a500a6b18995b03f44bb040a5ffc28e45cb0'
        USDC_ADDRESS = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

        WHITELISTED_POOLS = ['0xebdd200fe52997142215f7603bc28a80becdadeb000200000000000000000694']

        WHITE_LISTED_TOKENS = [OLAS_ADDRESS, USDC_ADDRESS]

        pools_of_interest = {}
        for pool_type in params:
            for pool_id in params[pool_type]:
                if pool_id.lower() in WHITELISTED_POOLS:
                    if pool_type not in pools_of_interest:
                        pools_of_interest[pool_type] = [pool_id]
                    else:
                        pools_of_interest[pool_type].append(pool_id)

        if not pools_of_interest:
            raise SorRetrievalException("No pools of interest found!")
        self.bal.getOnchainData(pools_of_interest)
        # We setup a mulkticall to ensure we have the name of all of the pools.

        self.bal.mc.reset()
        for token_address in self.bal.decimals:
            if token_address not in WHITE_LISTED_TOKENS:
                continue

            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                'name',
                args=[],
            )
        name_data = self.bal.mc.execute()

        # We now get the symbols
        self.bal.mc.reset()
        for token_address in self.bal.decimals:
            if token_address not in WHITE_LISTED_TOKENS:
                continue
            contract = self.bal.erc20GetContract(token_address)
            self.bal.mc.addCall(
                token_address,
                contract.abi,
                'symbol',
                args=[],
            )
        symbol_data = self.bal.mc.execute()

        for address, name, symbol in zip(self.bal.decimals, name_data[0], symbol_data[0]):
            print(address, name[0], symbol[0])
            # We now get get the price for the swap

        del args, kwargs

    def get_params_for_swap(self, input_token_address, output_token_address, input_amount):
        """
        Given the data, we get the params for the swap from the balancer exchange.
        """

    def get_price(self, input_token_address: str, output_token_address: str, amount: float) -> float:
        """
        Get the price of the token.
        """

        input_token = self.tokens[input_token_address]
        output_token = self.tokens[output_token_address]

        params = self.get_params_for_swap(
            input_token_address=input_token_address,
            output_token_address=output_token_address,
            amount_in=input_token.convert_to_decimals(input_token.convert_to_raw(amount)),
        )
        # we query the smart router
        sor_result = self.bal.balSorQuery(params)
        amount_out = float(sor_result['batchSwap']['limits'][-1])
        output_amount = -amount_out
        rate = Decimal(output_amount) / Decimal(amount)
        self.logger.info(
            f"""
                    Balancer Exchange on {self.chain_name}:;
                        input:
                            Amount: {amount}
                            Address: {input_token}
                        output:
                            Amount: {output_amount}
                            Address: {output_token}
                        Rate: {rate:.4f}"""
        )
        return rate

    async def fetch_ticker(self, *args, **kwargs):
        """
        Fetches a ticker.

        :return: The ticker.
        """
        del args, kwargs
        raise NotImplementedError

    async def fetch_positions(self, positions_message: PositionsMessage, dialogue: PositionsDialogue, **kwargs):
        """
        Fetches a ticker.

        :return: The ticker.
        """
        del kwargs
        return dialogue.reply(
            performative=PositionsMessage.Performative.ERROR,
            target_message=positions_message,
            error_code=PositionsMessage.ErrorCode.API_ERROR,
            error_msg="Spot exchange does not support positions!",
        )

    def get_price(self, input_token_address, output_token_address, amount):
        """
        get the price for a given input.
        """

        token_a = self.tokens.get(input_token_address)
        if not token_a:
            raise ValueError(f"Token {input_token_address} not found")
        token_b = self.tokens.get(output_token_address)
        if not token_b:
            raise ValueError(f"Token {output_token_address} not found")
        path, rate, total = self.loop.run_until_complete(
            self.get_path(token_a, token_b, amount)
        )
        self.last_trade_path = path
        self.logger.info(
            f"""
                    {self.exchange_type} Exchange;
                        input:
                            Amount: {amount}
                            Address: {token_a}
                        output:
                            Amount: {token_b.convert_to_decimals(total)}
                            Address: {token_b}
                        Rate: {rate:.6f}"""
        return Decimal(rate)

    def buy(self, token_a, token_b, amount, retries=99):
        """
        Buy token b with token a.
        """
        token_b, token_a = self.tokens.get(token_a), self.tokens.get(token_b)
        path, _, _ = self.loop.run_until_complete(
            self.get_path(token_a, token_b, amount_a=amount)
        )
        # if we were to store the last price here we could reduce the calls for buys.
        try:
            result = self._swap(amount, token_a, path)
        except ContractLogicError as error:
            self.logger.error(f"Failed to swap {token_a} for {token_b}")
            if retries > 0:
                time.sleep(1)
                return self.buy(token_b.address, token_a.address, amount, retries - 1)
            return False
        return result

    def sell(self, token_a, token_b, amount, retries=99):
        """
        Buy token b with token a.
        """
        token_a, token_b = self.tokens.get(token_a), self.tokens.get(token_b)
        path, _, _ = self.loop.run_until_complete(
            self.get_path(token_a, token_b, amount)
        )
        try:
            res = self._swap(amount, token_a, path)
        except ContractLogicError as error:
            self.logger.error(f"Failed to swap {token_a} for {token_b} {error}")
            if retries > 0:
                time.sleep(1)
                return self.sell(token_a.address, token_b.address, amount, retries - 1)
            return False
        return res

    def _swap(self, amount, token_a, path, retries=5):
        """
        Swap the tokens.
        """
        try:
            allowance = token_a.contract.functions.allowance(
                self.account.address, self.router_address
            ).call()

            if allowance < ((10**token_a.decimals) * amount):
                self.approve_permit_2(token_a, self.router_address)

            allowance = token_a.contract.functions.allowance(
                self.account.address, self.permit2_address
            ).call()
            self.logger.error("Failed to read allowance")
            if retries > 0:
                time.sleep(1)
                return self._swap(amount, token_a, path, retries - 1)
            raise ApprovalException("Failed to read allowance") from error

        if allowance < ((10**token_a.decimals) * amount):
            self.approve_permit_2(token_a, self.permit2_address)

        txn_data = self.loop.run_until_complete(
            self.build_transaction_data(path, amount, token_a)
        )
        txn = self.build_transaction(
            txn_data,
        )
        # we simulate the transaction
        try:
            self.web3.eth.call(txn)
        except Exception as error:
            self.logger.error("Failed to estimate gas! The transaction will revert!")
            if retries > 0:
                time.sleep(10)
                return self._swap(amount, token_a, path, retries - 1)
            raise error

        self.log(f"Sending transaction {txn}")
        result = self.do_tx(txn)
        if not result and retries > 0:
            self.logger.error(
                "Transaction failed to be successfully executed! Retrying"
            )
            time.sleep(5)
            return self._swap(amount, token_a, path, retries - 1)
        self.logger.info(f"Transaction hash: {result.hex()}")
        return result

    def build_transaction(self, txn_data):
        """
        Build the raw txn.
        """
        txn = {
            "from": self.account.address,
            "to": self.router_address,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
            "gas": 1_000_000,
            "gasPrice": int(self.web3.eth.gas_price * 1.1),
            "chainId": self.chain_id,
            "data": txn_data,
        }
        return txn

    async def build_transaction_data(
        self, path_obj, amount, token_a
    ):  # pylint: disable=too-many-locals
        """
        Build the transaction.
        """

        amount = float(amount)

        encoded_input = self.codec.encode.chain()

        for split in path_obj:
            function_name = split["function"]
            path = split["path"]
            estimated_amount = split["estimate"]
            weight = split["weight"] / 100

            _, _, p2_nonce = self.get_permit2_info(token_a)
            allowance_amount = 2**159 - 1  # max/infinite
            (
                permit_data,
                signable_message,
            ) = self.codec.create_permit2_signable_message(
                token_a.address,
                allowance_amount,
                self.codec.get_default_expiration(60 * 24 * 3600 * 10),  # 30 days
                p2_nonce,
                self.router_address,
                self.codec.get_default_deadline(18000),  # 180 seconds
                chain_id=self.chain_id,
            )

            signed_message = self.account.sign_message(signable_message)
            encoded_input = encoded_input.permit2_permit(permit_data, signed_message)

            if function_name == "V2_SWAP_EXACT_IN":
                encoded_input = encoded_input.v2_swap_exact_in(
                    FunctionRecipient.SENDER,
                    amount_in=int(amount * weight * (10**token_a.decimals)),
                    amount_out_min=int(estimated_amount * (1 - float(ALLOWED_SLIPPAGE))),
                    path=path,
                )
            elif function_name == "V3_SWAP_EXACT_IN":
                # we need to add the permit
                encoded_input = encoded_input.v3_swap_exact_in(
                    FunctionRecipient.SENDER,
                    amount_in=int(amount * weight * (10**token_a.decimals)),
                    amount_out_min=int(estimated_amount * (1 - float(ALLOWED_SLIPPAGE))),
                    path=path,
                )

        txn_data = encoded_input.build(
            self.codec.get_default_deadline(valid_duration=180000000),
        )
        return txn_data

    def get_permit2_info(self, token):
        """
        Get the permit2 info.
        """
        with open(
            "olas_arbitrage/abis/uniswap/permit2.json", encoding=DEFAULT_ENCODING
        ) as f:
            permit2_abi = json.load(f)
        permit2_contract = self.web3.eth.contract(
            address=self.permit2_address, abi=permit2_abi
        )
        p2_amount, p2_expiration, p2_nonce = permit2_contract.functions.allowance(
            self.account.address,
            token.address,
            self.router_address,
        ).call()
        return p2_amount, p2_expiration, p2_nonce

    def approve_permit_2(self, token, address):
        """
        Approve the token.
        """
        permit2_allowance = 2**200 - 1  # max
        contract_function = token.contract.functions.approve(
            address, int(permit2_allowance)
        )
        trx_params = contract_function.build_transaction(
            {
                "from": self.account.address,
                "gas": 500_000,
                "gasPrice": int(self.web3.eth.gas_price * 1.1),
                "chainId": self.chain_id,
                "value": 0,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
            }
        )
        if not self.do_tx(trx_params):
            raise ApprovalException("Failed to approve token")
        return True

    def do_approval(self, input_token_address: str, amount: float):
        """Do the necessary approval for the swap."""
        self.log("Step 1: Approve tokens")
        token_0 = self.tokens[input_token_address]
        # Uniswap router must be allowed to spent our quote token
        # we check if we have enough balance and if we have enough approval
        current_allowance = token_0.contract.functions.allowance(
            self.account.address, self.router_address
        ).call()
        if current_allowance < amount:
            # we set the allowance
            approve = token_0.contract.functions.approve(
                self.router_address, int(amount)
            )
            # we build the transaction
            tx_1 = approve.build_transaction(
                {
                    # we use the gase price * 1.05
                    "from": self.account.address,
                    "gasPrice": int(self.web3.eth.gas_price * 1.025),
                    "nonce": self.web3.eth.get_transaction_count(self.account.address),
                }
            )
            # we first sign the transaction
            signed_tx_1 = self.account.sign_transaction(tx_1)
            # we send the transaction
            tx_hash_1 = self.web3.eth.send_raw_transaction(signed_tx_1.rawTransaction)
            # we wait for the transaction to be mined
            self.log(f"Transaction hash: {tx_hash_1.hex()}")
            self.log("Waiting for transaction to be mined")
            # we wait for the next block to be sure that the transaction nonce is correct
            self.log("Waiting for next block")
            current_block = self.web3.eth.block_number
            while current_block == self.web3.eth.block_number:
                time.sleep(0.1)
            if not self.wait_for_transaction(tx_hash_1):
                self.logger.error("Approval transaction failed to be mined.")
                # we dont need to hard exit here.
                return False
        else:
            self.log("Token already approved")
        return True
