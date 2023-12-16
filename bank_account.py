import operator
from abc import ABC, abstractmethod
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


class BankAccount(ABC):
    """
    This class represents a User's bank account. It contains the information necessary
    for a user to record and view transactions.
    """
    def __init__(self, bank_acc_num: str, bank_name: str, bank_bal: float):
        self._bank_acc_num = bank_acc_num
        self._bank_name = bank_name
        self._bank_bal = bank_bal
        self._is_locked = False

    @property
    def bank_account_number(self):
        """
        Getter for bank account number.
        :return: bank account number
        """
        return self._bank_acc_num

    @property
    def bank_name(self):
        """
        Getter for bank name.
        :return: bank name
        """
        return self._bank_name

    @property
    def bank_bal(self):
        """
        Getter for bank balance.
        :return: bank balance
        """
        return self._bank_bal

    @property
    def is_locked(self):
        """
        Getter for the Boolean representing if the bank account is locked.
        :return: bool
        """
        return self._is_locked

    @bank_bal.setter
    def bank_bal(self, updated: float):
        """
        Setter for bank balance.
        :param updated: a float
        """
        if 0 < updated < 5:
            print("Notification: Your bank account balance is less than $5.")
        self._bank_bal = updated

    @is_locked.setter
    def is_locked(self, updated: bool) -> None:
        """
        Setter for is_locked attribute.
        :param updated: a boolean
        """
        self._is_locked = updated

    def lock_account(self):
        self._is_locked = True

    def is_balance_negative(self):
        """
        Locks the account if the bank balance became negative.
        """
        self.is_locked = True if self._bank_bal <= 0 else False
        if self._bank_bal <= 0:
            print("Locked: Your account is locked since the bank balance reached zero.")
            self.is_locked = True

    @abstractmethod
    def is_over_limit(self, transaction_catalogue):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Chequing(BankAccount):
    """
    Chequing BankAccount Class.
    """
    def __init__(self, bank_acc_num: str, bank_name: str, bank_bal: float):
        """
        Initialize the Chequing with a bank account number, bank name, and bank balance.
        :param bank_acc_num: a string
        :param bank_name: a string
        :param bank_bal: a float
        """
        super().__init__(bank_acc_num, bank_name, bank_bal)
        self._is_locked = False

    def is_over_limit(self, transaction_catalogue):
        pass

    def __repr__(self):
        print("--------- Bank Account Information ---------")
        message = (f"Bank Account Type: Chequing\n"
                   f"Bank Account Number: {self.bank_account_number}\n"
                   f"Bank Name: {self.bank_name}\n"
                   f"Bank Balance: ${self.bank_bal:.2f}\n"
                   f"Bank Account Locked: {self.is_locked}")
        return message


class Saving(BankAccount):
    """
    Saving BankAccount Class. There are additional restrictions imposed on savings accounts.
    Users may not make more than 2 transactions per calendar month.
    """
    MAX_TRANSACTIONS = 2

    def __init__(self, bank_acc_num: str, bank_name: str, bank_bal: float):
        """
        Initialize the Saving with a bank account number, bank name, and bank balance.
        :param bank_acc_num: a string
        :param bank_name: a string
        :param bank_bal: a float
        """
        super().__init__(bank_acc_num, bank_name, bank_bal)
        self._num_of_transaction = 0
        self._is_locked = False

    @property
    def num_of_transaction(self) -> int:
        """
        Returns the number of transaction.
        :return: an int
        """
        return self._num_of_transaction

    @num_of_transaction.setter
    def num_of_transaction(self, updated: int):
        """
        Update the number of transaction.
        :param updated: an int
        """
        self._num_of_transaction = updated

    @staticmethod
    def get_one_month_ago() -> time:
        """
        Get datetime one month ago
        :return: a datetime
        """
        current = datetime.now()
        last_month = current - relativedelta(months=1)
        return last_month

    def is_over_limit(self, transaction_catalogue) -> None:
        """
        Lock the account if the latest transaction is occurred within a month and the number of
        transaction gets to the limit.
        """
        catalogue = transaction_catalogue
        transaction_list = catalogue.get_user_transactions(self.bank_account_number)
        sorted_list = sorted(transaction_list, key=operator.attrgetter("time"))

        transaction_list = [transaction for transaction in sorted_list
                            if datetime.strptime(transaction.time, '%Y-%m-%d %H:%M:%S') > self.get_one_month_ago()]

        self.num_of_transaction = len(transaction_list)

        if self.num_of_transaction >= self.MAX_TRANSACTIONS:
            print("Locked: Your account is locked.")
            self.is_locked = True
        else:
            self.is_locked = False

    def __repr__(self):
        print("======== Bank Account Information ========")
        message = (f"Bank Account Type: Saving\n"
                   f"Bank Account Number: {self.bank_account_number}\n"
                   f"Bank Name: {self.bank_name}\n"
                   f"Bank Balance: ${self.bank_bal:.2f}\n"
                   f"Bank Account Locked: {self.is_locked}")
        return message
