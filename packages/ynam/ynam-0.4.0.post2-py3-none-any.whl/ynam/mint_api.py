import ast
import inspect
from dataclasses import dataclass

from mintapi import RESTClient, SeleniumBrowser

from .ynam_parser import arg
from .ynam_parser import logger
from .ynam_secrets import get_stash
from .ynab_api import YNABTransaction


@dataclass
class MintTransaction:

    date: str
    amount: int
    inferredDescription: str
    id: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v
            for k, v in env.items() if k in inspect.signature(cls).parameters
        })

    def asYNAB(self):
        return YNABTransaction(
            **{
                "date": self.date,
                "amount": int(self.amount * 1000),
                "account_id": get_stash().ynab_account_id,
                "payee_name": self.inferredDescription,
                "import_id": self.id,
            })


class MintAPI():

    def __init__(self) -> None:
        self.restClient = RESTClient
        self.browser = SeleniumBrowser
        self.cpath = arg('mint_cookies')
        self.keypath = arg('mint_api_key_file')

    def get_transactions(self, start_date: str = None):
        client = self.restClient()
        client.authorize(self.cookies(), self.key())
        items = client.get_transaction_data()

        logger.info(f"Found {len(items)} transactions in Mint.")
        [logger.debug(item['fiData']) for item in items]

        items = [
            MintTransaction.from_dict(item['fiData']) for item in items
        ]
        items = [item for item in items if item.date > start_date]
        return items

    def cookies(self):
        with open(self.cpath, 'r') as file:
            return ast.literal_eval(file.read())

    def key(self):
        with open(self.keypath, 'r') as file:
            return ast.literal_eval(file.read())['authorization']

    def updateAuth(self):
        stash = get_stash()
        browser = self.browser(
            email=stash.mint_username,
            password=stash.mint_password,
            mfa_method='soft-token',
            mfa_token=stash.mint_mfa_seed,
            use_chromedriver_on_path=arg('use_chromedriver_on_path'),
            headless=arg('headless'),
            wait_for_sync=False,
            wait_for_sync_timeout=10,
        )
        cookies = browser._get_cookies()
        with open(arg('mint_cookies'), 'w+') as file:
            file.write(str(cookies))

        api_key = browser._get_api_key_header()
        with open(arg('mint_api_key_file'), 'w+') as file:
            file.write(str(api_key))
