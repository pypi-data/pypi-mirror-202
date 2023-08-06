from dataclasses import dataclass, asdict
from inspect import signature as inspectSignature
from json import dumps as dumpJson
from json import loads as loadJson
from typing import List, Dict, Callable

from requests import Response, get, patch, post, put
# flake8: noqa

from .ynam_parser import logger


@dataclass
class YNABTransaction:

    date: str
    amount: int
    import_id: str
    account_id: str
    payee_name: str
    memo: str = None
    cleared: str = None
    approved: str = None
    payee_id: str = None
    flag_color: str = None
    category_id: str = None
    subtransactions: list = None
    cleared: str = 'cleared'

    def __post_init__(self) -> None:
        if len(self.payee_name) >= 100:
            shorter_name = self.payee_name[:100]
            logger.debug(
                f'Payee name "{self.payee_name}" too long. Shortened to "{shorter_name}')
            self.payee_name = shorter_name

    def asdict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v
            for k, v in env.items() if k in inspectSignature(cls).parameters
        })


class YNABAPI():
    def __init__(self, api_key: str) -> None:
        if api_key is None:
            raise ValueError(
                'Attempted to initialize YNAB API without API key.'
            )

        self.uri = 'https://api.youneedabudget.com/v1'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.budget_id: str = None

        logger.debug(f'YNABAPI uri: {self.uri}')
        logger.debug(f'YNABAPI headers: {self.headers}')

    def __call(self, call: Callable, url: str, **kwargs) -> dict:
        longstr = [f'\nkey: {k},\n value: {v}' for k, v in kwargs.items()]
        longstr = ' '.join(longstr)
        msg = f'Sending {call.__name__.upper()} to endpoint {url} '
        msg += f"using kwargs: {longstr if len(longstr) > 0 else None}"
        logger.debug(msg)

        results: Response = call(self.uri + url, **kwargs, headers=self.headers)
        jsonResults: dict = loadJson(results.content.decode('utf-8'))
        if 'data' in jsonResults.keys():
            logger.debug('Call successful!')
            logger.debug(jsonResults)
            return jsonResults['data']
        else:
            logger.warn(
                f"Found error {jsonResults['error']} in response body.")
            raise Exception(jsonResults['error'])

    def _patch(self, url: str, **kwargs) -> dict:
        return self.__call(patch, url, **kwargs)

    def _post(self, url: str, **kwargs) -> dict:
        return self.__call(post, url, **kwargs)

    def _put(self, url: str, **kwargs) -> dict:
        return self.__call(put, url, **kwargs)

    def _get(self, url: str, **kwargs) -> dict:
        return self.__call(get, url, **kwargs)

# User

    def get_user(self) -> dict:
        """Returns authenticated user information
        """
        return self._get(f'/user')['user']

# Budgets

    def get_budgets(self) -> dict:
        """List budgets

        Returns:
          dict: budgets list with summary information
        """
        return self._get(url='/budgets')['budgets']

    def get_budget(self, budget_id: str = None) -> dict:
        """Returns a single budget with all related entities.
        This resource is effectively a full budget export.

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
          dict: single budget
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}'
        return self._get(url=url)['budget']

    def get_budget_settings(self, budget_id: str = None) -> dict:
        """Returns a single budget with all related entities.
        This resource is effectively a full budget export.

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
          dict: settings for a budget
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/settings'
        return self._get(url=url)['settings']

# Accounts

    def get_accounts(self, budget_id: str = None) -> dict:
        """Account list

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all accounts
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/accounts'
        return self._get(url)['accounts']

    def get_account(self, account_id: str, budget_id: str = None) -> dict:
        """Account list

        Args:
            account_id (str): The id of the account
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all accounts
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/accounts/{account_id}'
        return self._get(url)['account']

    def post_account(self,
                     name: str,
                     type: str,
                     balance: int,
                     budget_id: str = None) -> dict:
        """Create a new account

        Args:
            name (str): the name of the account
            type (str): the type of account
            balance (int): the current balance of the account in milliunits format
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: the created account
        """
        if type not in _account_types:
            raise InvalidAccountType(
                f'The valid account types are {_account_types}')

        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/accounts'
        json = {"account": {"name": name, "type": type, "balance": balance}}
        results = self._post(url, json=json)
        return results

# Categories

    def get_categories(self, budget_id: str = None) -> dict:
        """List categories

        Amounts (budgeted, activity, balance, etc.) are specific to the current budget month (UTC).

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
          dict: all categories grouped by category group.
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/categories'
        results = self._get(url=url)
        return results['category_groups']

    def get_category(self, category_id: str, budget_id: str = None) -> dict:
        """Single category

        Args:
            category_id (str): The id of the category
              budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
              last used budget and “default” can be used if default budget selection is enabled.
              If not specified, defaults to self.budget_id

        Returns:
            dict: The requested category
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/categories/{category_id}'
        return self._get(url=url)['category']

    def get_category_by_month(self,
                              category_id: str,
                              month: str,
                              budget_id: str = None) -> dict:
        """Single category for a specific budget month.

        Args:
            category_id (str): The id of the category
            month (str): The budget month in ISO format (e.g. 2016-12-01)
            (“current” can also be used to specify the current calendar month (UTC))
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: The requested month category
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/months/{month}/categories/{category_id}'
        return self._get(url=url)['category']

    # this one returns a 500 error for some reason
    def patch_category_by_month(self,
                                category_id: str,
                                month: str,
                                budgeted_amount: int,
                                budget_id: str = None) -> dict:
        """Update a category for a specific month. Only budgeted amount can be updated.

        Args:
            category_id (str): The id of the category
            month (str): The budget month in ISO format (e.g. 2016-12-01)
            (“current” can also be used to specify the current calendar month (UTC))
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: The updated category
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/months/{month}/categories/{category_id}'
        data = {"category": {"budgeted": budgeted_amount}}
        return self._patch(url=url, data=data)

# Payees

    def get_payees(self, budget_id: str = None) -> dict:
        """List payees

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all payees
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/payees'
        return self._get(url=url)['payees']

    def get_payee(self, payee_id: str, budget_id: str = None) -> dict:
        """Single payee

        Args:
            payee_id (str): The id of the payee
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all payees
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/payees/{payee_id}'
        return self._get(url=url)['payee']

# Payee Locations

    def get_payee_locations(self, budget_id: str = None) -> dict:
        """List payee locations

        When you enter a transaction and specify a payee on the YNAB mobile apps,
        the GPS coordinates for that location are stored, with your permission,
        so that the next time you are in the same place (like the Grocery store)
        we can pre-populate nearby payees for you! It's handy and saves you time.
        This resource makes these locations available.
        Locations will not be available for all payees.

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all payee locations
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/payee_locations'
        return self._get(url=url)['payee_locations']

    def get_payee_location(self,
                           payee_location_id: str,
                           budget_id: str = None) -> dict:
        """Single payee location

        When you enter a transaction and specify a payee on the YNAB mobile apps,
        the GPS coordinates for that location are stored, with your permission,
        so that the next time you are in the same place (like the Grocery store)
        we can pre-populate nearby payees for you! It's handy and saves you time.
        This resource makes these locations available.
        Locations will not be available for all payees.

        Args:
            payee_location_id (str): id of payee location
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all payee locations
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/payee_locations/{payee_location_id}'
        results = self._get(url=url)
        return results['payee_locations']

    def get_locations_for_payee(self,
                                payee_id: str,
                                budget_id: str = None) -> dict:
        """List locations for a payee

        When you enter a transaction and specify a payee on the YNAB mobile apps,
        the GPS coordinates for that location are stored, with your permission,
        so that the next time you are in the same place (like the Grocery store)
        we can pre-populate nearby payees for you! It's handy and saves you time.
        This resource makes these locations available.
        Locations will not be available for all payees.

        Args:
            payee_location_id (str): id of payee
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all payee locations for a specified payee
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/payee_locations/{payee_id}'
        return self._get(url=url)['payee_locations']

# Months

    def get_months(self, budget_id: str = None) -> dict:
        """List budget months

        Each budget contains one or more months, which is where Ready to Assign,
        Age of Money and category (budgeted / activity / balances) amounts are available.

        Args:
              budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
              last used budget and “default” can be used if default budget selection is enabled.
              If not specified, defaults to self.budget_id

        Returns:
          dict: all budget months
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/months'
        return self._get(url=url)['months']

    def get_month(self, month: str, budget_id: str = None) -> dict:
        """Single budget month

        Args:
              month (str): The budget month in ISO format (e.g. 2016-12-01)
              (“current” can also be used to specify the current calendar month (UTC))
              budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
              last used budget and “default” can be used if default budget selection is enabled.
              If not specified, defaults to self.budget_id

        Returns:
          dict: a single budget month
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/months/{month}'
        return self._get(url=url)['month']

# Transactions

    def get_transactions(
        self,
        since_date: str = None,
        type: str = None,
        budget_id: str = None,
    ) -> Dict[str, List[YNABTransaction]]:
        """List transactions as YNABTransactions.

        Args:
            since_date (str, optional): If specified, only transactions on or after this date will be included.
            The date should be ISO formatted (e.g. 2016-12-30).
            type (str, optional): If specified, only transactions of the specified type will be included.
            “uncategorized” and “unapproved” are currently supported.
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id
        Returns:
            Dict[str, List[YNABTransaction]]: budget transactions
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions'
        data = {"since_date": since_date, "type": type}
        # result = self._get(url)
        result = self._get(url, json=data)
        return [
            YNABTransaction.from_dict(xt)
            for xt in result['transactions']
        ]

    def get_transaction(
        self,
        transaction_id: str,
        budget_id: str = None,
    ) -> Dict[str, YNABTransaction]:
        """Single transaction

        Args:
            transaction_id (str): The id of the transaction
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            Dict[str, YNABTransaction]: requested transaction
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions/{transaction_id}'
        results = self._get(url)
        return results['transaction']

    def get_account_transactions(
        self,
        account_id: str,
        budget_id: str = None,
        since_date: str = None,
        type: str = None,
    ) -> Dict[str, YNABTransaction]:
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/accounts/{account_id}/transactions'
        data = {
            "account_id": account_id,
            "since_date": since_date,
            "type": type,
        }
        result = self._get(url, json=data)
        return [
            YNABTransaction.from_dict(xt)
            for xt in result['transactions']
        ]

    def get_category_transactions(
        self,
        category_id: str,
        budget_id: str = None,
        since_date: str = None,
        type: str = None,
    ) -> Dict[str, YNABTransaction]:
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions/{category_id}'
        data = {
            "category_id": category_id,
            "since_date": since_date,
            "type": type,
        }
        result = self._get(url, json=data)
        return [
            YNABTransaction.from_dict(xt)
            for xt in result['transactions']
        ]

    def get_payee_transactions(
        self,
        payee_id: str,
        budget_id: str = None,
        since_date: str = None,
        type: str = None,
    ) -> Dict[str, YNABTransaction]:
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions/{payee_id}'
        data = {
            "category_id": payee_id,
            "since_date": since_date,
            "type": type,
        }
        result = self._get(url, json=data)
        return [
            YNABTransaction.from_dict(xt)
            for xt in result['transactions']
        ]

    def put_transaction(
        self,
        transaction_id: str,
        updated_transaction: YNABTransaction,
        budget_id: str = None,
    ) -> Dict[str, YNABTransaction]:
        """Updates a single transaction

        Args:
            transaction_id (str): The id of the transaction
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id
            updated_transaction (YNABTransaction): transaction with new values

        Returns:
            Dict[str, YNABTransaction]: updated transaction
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions/{transaction_id}'
        data = {"transaction": updated_transaction}
        results = self._put(url, json=data)
        return results

    def post_transactions(
        self,
        transactions: YNABTransaction or List[YNABTransaction],
        budget_id: str = None,
    ) -> dict:
        """Create a single transaction or multiple transactions.
        Scheduled transactions cannot be created on this endpoint.

        Args:
            transactions (YNABTransaction or List[YNABTransaction]): either single transaction or list of transactions

        Returns:
            dict: successfully created transactions
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions'
        data = {"transactions": transactions}
        results = self._post(url, json=data)
        return results

    def post_import_transactions(
        self,
        transactions: YNABTransaction or List[YNABTransaction],
        budget_id: str = None,
    ) -> dict:
        """Same as post_transactions, but sent to the Import endpoint.

        Args:
            transactions (YNABTransaction or List[YNABTransaction]): _description_
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions/import'
        json = {"transactions": transactions}
        results = self._post(url, json=json)
        return results

    def patch_transactions(
        self,
        transactions: YNABTransaction or List[YNABTransaction],
        budget_id: str = None,
    ) -> dict:
        """Updates multiple transactions, by id or import_id.

        Args:
            transactions (YNABTransaction or List[YNABTransaction]): either single transaction or list of transactions

        Returns:
            dict: successfully updated transactions
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions'
        json = {"transactions": transactions}
        results = self._patch(url, json=json)
        return results

    def print_transactions(
        self,
        since_date: str = '',
        type: str = '',
        budget_id: str = None,
    ) -> None:
        """Same as get_transactions, but prints to console
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/transactions'
        data = {
            "since_date": since_date,
            "type": type,
        }
        result = self._get(url, json=data)
        print(
            dumpJson(([xt for xt in result['transactions']]),
                     indent=2))

    def get_scheduled_transactions(
        self,
        budget_id: str = None,
    ) -> Dict[str, list]:
        """List scheduled transactions

        Args:
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            dict: all scheduled transactions
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/scheduled_transactions'
        results = self._get(url)
        return results['scheduled_transactions']

    def get_scheduled_transaction(
        self,
        scheduled_transaction_id: str,
        budget_id: str = None,
    ) -> Dict[str, list]:
        """Single scheduled transaction

        Args:
            scheduled_transaction_id (str): The id of the scheduled transaction
            budget_id (str, optional): The id of the budget. “last-used” can be used to specify the
            last used budget and “default” can be used if default budget selection is enabled.
            If not specified, defaults to self.budget_id

        Returns:
            Dict[str, YNABTransaction]: a single scheduled transaction
        """
        budget_id = _oneOf(budget_id, self.budget_id)
        url = f'/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}'
        results = self._get(url)
        return results['scheduled_transaction']


def _oneOf(this, that):
    return that if this is None else this


_account_types = [
    "checking",
    "savings",
    "cash",
    "creditCard",
    "lineOfCredit",
    "otherAsset",
    "otherLiability",
    "mortgage",
    "autoLoan",
    "studentLoan",
    "personalLoan",
    "medicalDebt",
    "otherDebt",
]


class InvalidAccountType(Exception):
    pass


def __stringify(**kwargs) -> list:
    return [f'\nkey: {k},\n value: {v}' for k, v in kwargs.items()]
