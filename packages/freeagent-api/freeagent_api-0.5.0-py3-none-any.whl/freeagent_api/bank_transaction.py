"""Module for interacting with FreeAgent bank account transaction data."""
from freeagent_api.base_object import BaseObject
from freeagent_api.bank_transaction_explanation import BankTransactionExplanation


class BankTransaction(BaseObject):
    """Representation of a bank account transaction.

    See https://dev.freeagent.com/docs/bank_transactions
    """

    API_FIELDS = [
        "url",
        "amount:decimal",
        "bank_account:id",
        "dated_on:date",
        "description",
        "full_description",
        "uploaded_at:datetime",
        "unexplained_amount:decimal",
        "is_manual:boolean",
        "transaction_id", # String assigned by the bank, *NOT* a FreeAgent assigned ID
        "created_at:datetime",
        "updated_at:datetime",
        "matching_transactions_count:integer",
        #"bank_transaction_explanations", # array of BankTransactionExplanation, overridden to 'explanations'
        "explanations",
    ]


    def __init__(self, data = None):
        """Initialise the BankTransaction object.

        Converts the explanations from dict to object.
        """
        super().__init__(data)
        if data:
            self._data['explanations'] = []
            for item_data in data['bank_transaction_explanations']:
                self._data['explanations'].append(BankTransactionExplanation(item_data))
