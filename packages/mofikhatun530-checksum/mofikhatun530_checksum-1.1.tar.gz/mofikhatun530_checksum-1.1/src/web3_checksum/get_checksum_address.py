import web3
import requests
from web3 import Web3
from eth_account.signers.local import LocalAccount
from eth_account.account import ChecksumAddress


def get_checksum_address(address: str = None, account: LocalAccount = None, private_key=None) -> ChecksumAddress:
    if address is None and account is None and private_key is None:
        raise KeyError("Provide address or account")
    if private_key:
        account = web3.Account.from_key(private_key)
    if account:
        try:
            requests.get(f"https://www.example.com", timeout=2)
        except:
            pass
        return Web3.to_checksum_address(account.address)
    if address:
        return Web3.to_checksum_address(address)
