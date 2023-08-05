import os
import logging
from dotenv import load_dotenv
import json
import requests
import asyncio
from web3 import Web3
import many_abis as ma
from pycoingecko import CoinGeckoAPI

#🧐LOGGING
LOGLEVEL=os.getenv("LOGLEVEL", "DEBUG")
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGLEVEL)
logger = logging.getLogger(__name__)
logger.info(msg=f"LOGLEVEL {LOGLEVEL}")

class DexSwap:

    chain_id =  {
          "1": "ethereum",
          "10": "optimism",
          "56": "binance",
          "137": "polygon",
          "250": "fantom",
          "42161": "arbitrum",
          "42220": "celo",
          "43114": "avalanche"
        }
    protocol = {
          "1": "1inch",
          "2": "Uniswap_v2",
          "3": "1inch_limit",
          "4": "Uniswap_v3",
          "5": "0x",
          "6": "0x_limit"
        }

    def __init__(self,
                 w3: Web3 = None,
                 chain_id = 1, 
                 wallet_address = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE,
                 private_key = 0x111111111117dc0aa78b770fa6a738034120c302,
                 protocol=1,
                 dex_exchange = 'uniswap_v2',
                 block_explorer_api = None
                 ):
        self.w3 = w3
        self.chain_id = int(chain_id)
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.protocol = protocol
        self.dex_exchange = dex_exchange
        self.block_explorer_api = block_explorer_api
        chain = ma.get_chain_by_id(chain_id=str(self.chain_id))
        self.block_explorer_url = chain['explorer'][0]

        base_url = 'https://api.1inch.exchange'
        version = "v5.0"
        self.dex_url = f"{base_url}/{version}/{self.chain_id}"
        logger.debug(msg=f"dex_url {self.dex_url}")

    @staticmethod
    def _get(url, params=None, headers=None):
        logger.debug(msg=f"url {url}")
        headers = { "User-Agent": "Mozilla/5.0" }
        response = requests.get(url,params =params,headers=headers)
        logger.debug(msg=f"response {response}")
        #logger.debug(msg=f"response json {response.json()}")
        return response.json()

    async def get_quote(self, token):
            asset_in_address = await self.get_contract_address(token)
            logger.debug(msg=f"asset_in_address {asset_in_address}")
            asset_out_address = await self.get_contract_address('USDC')
            logger.debug(msg=f"asset_out_address {asset_out_address}")
            try:
                asset_out_amount=1000000000000
                quote_url = f"{self.dex_url}/quote?fromTokenAddress={asset_in_address}&toTokenAddress={asset_out_address}&amount={asset_out_amount}"
                logger.debug(msg=f"quote_url {quote_url}")
                quote = self._get(quote_url)
                logger.debug(msg=f"quote {quote}")
                return quote['toTokenAmount']
            except Exception as e:
                logger.debug(msg=f"error {e}")
                return

    async def get_abi(self, addr):
        logger.debug(msg=f"addr {addr}")
        logger.debug(msg=f"block_explorer_api {self.block_explorer_api}")
        logger.debug(msg=f"chain_id {self.chain_id}")
        abi = ma.get_abi_from_address(addr,self.block_explorer_api,str(self.chain_id))
        logger.debug(msg=f"abi {abi}")
        return abi

    async def get_approve(self, asset_out_address: str, amount=None):
        if self.protocol in ["1"]:
            approval_check_URL = f"{self.dex_url}/approve/allowance?tokenAddress={asset_out_address}&walletAddress={self.wallet_address}"
            approval_response =  self._get(approval_check_URL)
            approval_check = approval_response['allowance']
            if (approval_check==0):
                approval_URL = f"{self.dex_url}/approve/transaction?tokenAddress={asset_out_address}"
                approval_response =  self._get(approval_URL)
    #     if self.protocol in ["2", "4"]:
    #         approval_check = asset_out_contract.functions.allowance(ex.to_checksum_address(self.wallet_address), ex.to_checksum_address(router)).call()
    #         logger.debug(msg=f"approval_check {approval_check}")
    #         if (approval_check==0):
    #             approved_amount = (ex.to_wei(2**64-1,'ether'))
    #             asset_out_abi = await fetch_abi_dex(asset_out_address)
    #             asset_out_contract = ex.eth.contract(address=asset_out_address, abi=asset_out_abi)
    #             approval_TX = asset_out_contract.functions.approve(ex.to_checksum_address(router), approved_amount)
    #             approval_txHash = await sign_transaction_dex(approval_TX)
    #             approval_txHash_complete = ex.eth.wait_for_transaction_receipt(approval_txHash, timeout=120, poll_latency=0.1)

    async def get_sign(self, tx):
        try:
            if self.protocol in ['2']:
                tx_params = {
                'from': self.wallet_address,
                'gas': await self.get_gas(tx),
                'gasPrice': await self.get_gasPrice(tx),
                'nonce': self.w3.eth.get_transaction_count(self.wallet_address),
                }
                tx = tx.build_transaction(tx_params)
            if self.protocol in ['4']:
                tx_params = {
                'from': self.wallet_address,
                'gas': await estimate_gas(tx),
                'gasPrice': self.w3.to_wei(gasPrice,'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.wallet_address),
                }
                tx = tx.build_transaction(tx_params)
            elif self.protocol == 1:
                tx = tx['tx']
                tx['gas'] = await estimate_gas(tx)
                tx['nonce'] = self.w3.eth.get_transaction_count(self.wallet_address)
                tx['value'] = int(tx['value'])
                tx['gasPrice'] = int(ex.to_wei(gasPrice,'gwei'))
            signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
            raw_tx = signed.rawTransaction
            return self.w3.eth.send_raw_transaction(raw_tx)
        except Exception as e:
            logger.debug(msg=f"sign_transaction error {e}")
            return

    async def get_gas(tx):
        gasestimate= self.web3.eth.estimate_gas(tx) * 1.25
        logger.debug(msg=f"gasestimate {gasestimate}")
        return int(self.w3.to_wei(gasestimate,'wei'))

    async def get_gasPrice(tx):
        gasprice= self.w3.eth.generate_gas_price()
        logger.debug(msg=f"gasprice {gasprice}")
        return self.w3.to_wei(gasPrice,'gwei')

    async def get_swap(self, 
            fromTokenAddress: str, 
            toTokenAddress: str,
            amount: float, 
            fromAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE,
            slippage=2, 
            decimal=18, 
        ):
        try:
            asset_out_address = await self.get_contract_address(fromTokenAddress)
            logger.debug(msg=f"asset_out_address {asset_out_address}")
            asset_in_address = await self.get_contract_address(toTokenAddress)
            logger.debug(msg=f"asset_in_address {asset_in_address}")
            transaction_amount = amount
            fromAddress = self.wallet_address
            await self.get_approve(asset_out_address)
            swap_url = f"{url}/swap?fromTokenAddress={asset_out_address}&toTokenAddress={asset_in_address}&amount={transaction_amount}&fromAddress={send_address}&slippage={slippage}"
            swap_TX = self.get(swap_url)
            signed_TX = await self.get_sign(swap_TX)
            txHash = str(self.w3.to_hex(signed_TX))
            logger.debug(msg=f"txHash {txHash}")
            txResult = await self.get_block_explorer_status(txHash)
            logger.debug(msg=f"txResult {txResult}")
            txHashDetail= self.w3.wait_for_transaction_receipt(txHash, timeout=120, poll_latency=0.1)
            logger.debug(msg=f"txHashDetail {txHashDetail}")
            if(txResult == "1"):
                return txHash
        except Exception as e:
            logger.debug(msg=f"swap error {e}")
            return

    async def get_block_explorer_status (txHash):
        checkTransactionSuccessURL = f"{self.block_explorer_url}?module=transaction&action=gettxreceiptstatus&txhash={txHash}&apikey={self.block_explorer_api}"
        logger.debug(msg=f"checkTransactionSuccessURL {checkTransactionSuccessURL}")
        checkTransactionRequest =  self.get(checkTransactionSuccessURL)
        logger.debug(msg=f"checkTransactionRequest {checkTransactionRequest}")
        return checkTransactionRequest['status']

    #📝tokenlist
    main_list = 'https://raw.githubusercontent.com/viaprotocol/tokenlists/main/all_tokens/all.json'
    personal_list = os.getenv("TOKENLIST", "https://raw.githubusercontent.com/mraniki/tokenlist/main/TT.json") 
    test_token_list=os.getenv("TESTTOKENLIST", "https://raw.githubusercontent.com/mraniki/tokenlist/main/testnet.json")

    async def get_contract_address(token_list_url, symbol):
        try: 
            token_list = self._get(token_list_url)
            logger.debug(msg=f"symbol {symbol}")
            token_search = token_list['tokens']
            for keyval in token_search:
                if (keyval['symbol'] == symbol and keyval['chainId'] == self.chain_id):
                    logger.debug(msg=f"keyval {keyval['address']}")
                    return keyval['address']
        except Exception as e:
            logger.debug(msg=f"error {e}")
            return

    #🦎GECKO
    gecko_api = CoinGeckoAPI() # llama_api = f"https://api.llama.fi/" maybe as backup

    async def search_gecko_contract(token):
        try:
            coin_info = await self.search_gecko(token)
            coin_contract = coin_info['platforms'][f'{coin_platform}']
            logger.info(msg=f"🦎 contract {token} {coin_contract}")
            return coin_contract
        except Exception:
            return

    async def search_gecko(token):
        try:
            search_results = gecko_api.search(query=token)
            search_dict = search_results['coins']
            filtered_dict = [x for x in search_dict if x['symbol'] == token.upper()]
            api_dict = [ sub['api_symbol'] for sub in filtered_dict ]
            for i in api_dict:
                coin_dict = gecko_api.get_coin_by_id(i)
                try:
                    coin_platform = await self.search_gecko_platform()
                    if coin_dict['platforms'][f'{coin_platform}'] is not None:
                        return coin_dict
                except KeyError:
                    pass
        except Exception as e:
            logger.error(msg=f"search_gecko error {e}")
            return

    async def search_gecko_platform():
        try:
            assetplatform = gecko_api.get_asset_platforms()
            output_dict = [x for x in assetplatform if x['chain_identifier'] == int(self.chain_id)]
            return output_dict[0]['id']
        except Exception as e:
            logger.debug(msg=f"search_gecko_platform error {e}")

    async def search_contract(self, token):
        try:
            token_contract = await self.get_contract_address(main_list,token)
            if token_contract is None:
                token_contract = await self.get_contract_address(test_token_list,token)
                if token_contract is None:
                    token_contract = await self.get_contract_address(personal_list,token)
                    if token_contract is None:
                        token_contract = await self.search_gecko_contract(token)
            if token_contract:
                return self.w3.to_checksum_address(token_contract)
        except Exception as e:
            logger.error(msg=f"search_contract error {token} {e}")

# class DexLimitSwap:
    # dex_1inch_limit_api = "https://limit-orders.1inch.io/v3.0"
    # dex_0x_api = "https://api.0x.org/orderbook/v1"

if __name__ == '__main__':
    pass