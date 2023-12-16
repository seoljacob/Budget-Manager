from budget_types import BudgetType
import time


class Transaction:
    """
    This class represents a transaction.
    """

    def __init__(self, timestamp: time, amount: float, budget_category: int, merchant: str, bank_num: str):
        """
        Constructor for Transaction class.
        :param timestamp: time when transaction was recorded
        :param amount: amount of transaction
        :param budget_category: budget category of transaction
        :param merchant: merchant of transaction
        :param bank_num: bank number of user
        """
        self.time = timestamp
        self.amount = amount
        self.budget_category = budget_category
        self.merchant = merchant
        self.bank_num = bank_num

    def __str__(self):
        """
        String representation of Transaction class.
        :return: a string
        """
        return f"\nTransaction:\n" \
               f"Time: {self.time} \n" \
               f"Amount: ${self.amount:.2f}\n" \
               f"Budget Category: {BudgetType(self.budget_category).name}\n" \
               f"Merchant: {self.merchant}\n" \
               f"Bank Number: {self.bank_num}"
