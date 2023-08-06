"""Module for interacting with FreeAgent transaction explanation data."""
from freeagent_api.base_object import BaseObject


class BankTransactionExplanation(BaseObject):
    """Representation of a bank account transaction explanation.

    See https://dev.freeagent.com/docs/bank_transaction_explanations
    """

    API_FIELDS = [
        "url",
        "bank_account:id",
        "bank_transaction:id",
        "type",
        "ec_status",
        "place_of_supply",
        "dated_on:date",
        "gross_value:decimal",
        "sales_tax_rate:decimal",
        "second_sales_tax_rate:decimal",
        "sales_tax_value:decimal",
        "second_sales_tax_value:decimal",
        "sales_tax_status",
        "second_sales_tax_status",
        "description",
        "category:id", # AccountingCategory object
        "cheque_number",
        "attachment", # TODO: parse attachments
        "marked_for_review:boolean",
        "is_money_in:boolean",
        "is_money_out:boolean",
        "is_money_paid_to_user:boolean",
        "is_locked:boolean",
        "locked_attributes", # array
        "locked_reason",
        "is_deletable:boolean",
        "project:id",
        "rebill_type",
        "rebill_factor:decimal",
        "receipt_reference",
        "paid_invoice:id",
        "foreign_currency_value:decimal",
        "paid_bill:id",
        "paid_user:id",
        "transfer_bank_account:id",
        "stock_item:id",
        "stock_altering_quantity:integer",
        "capital_asset:id",
        "asset_life_years:integer",
        "disposed_asset:id",
        "property:id",
    ]
