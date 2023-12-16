from abc import ABC, abstractmethod
from datetime import datetime


class User(ABC):
    """
    This class represents a single user (AKA a single child).
    """
    def __init__(self, name: str, dob: datetime, bank_account_number: str, warning_threshold):
        self._name = name
        self._dob = dob
        self._bank_account_number = bank_account_number
        self._warning_threshold = warning_threshold

    @property
    def name(self) -> str:
        """
        Return the name of the User
        :return: a string representing the user's name
        """
        return self._name

    @property
    def dob(self) -> datetime:
        """
        Return the dob of the User.
        :return: a datetime representing the user's birthday
        """
        return self._dob

    @property
    def bank_account_number(self) -> str:
        """
        Return the bank account number of the User.
        :return: a string representing the user's bank account number
        """
        return self._bank_account_number

    @abstractmethod
    def is_over_account_lockout_threshold(self, number_of_locked_budget, num_budget_types):
        """ Overrides to set the lock-out rule according to the user type. """
        pass

    @abstractmethod
    def is_over_lockout_threshold(self, limit, spent):
        """ Overrides to set the lock-out rule according to the user type. """
        pass

    @abstractmethod
    def is_lockout_action_required(self):
        """ Overrides to set the lock-out rule according to the user type. """
        pass

    @abstractmethod
    def lockout_msg(self):
        """ Overrides to set the lock-out rule according to the user type. """
        pass

    @abstractmethod
    def is_exceed_warning_threshold(self, limit, spent):
        """ Overrides to set the lock-out rule according to the user type. """
        pass

    @abstractmethod
    def warning_msg(self):
        """ Overrides to set the lock-out rule according to the user type. """
        pass

    def __str__(self):
        return (f"---- {type(self).__name__} ----\n"
                f"name: {self._name}\n" +
                f"dob: {self._dob}\n" +
                f"bank account number: {self._bank_account_number}")


class Angel(User):
    """
    An Angel class.
    """
    def __init__(self, name: str, dob: datetime, bank_account_number: str, warning_threshold: float):
        super().__init__(name, dob, bank_account_number, warning_threshold)

    def is_over_account_lockout_threshold(self, number_of_locked_budget, num_budget_types):
        """
        Returns always false.
        :param number_of_locked_budget: an int
        :param num_budget_types: an int
        :return: a boolean
        """
        return False

    def is_over_lockout_threshold(self, limit, spent):
        """
        Return True if the user exceed a budget category, otherwise False.
        :param limit: an int
        :param spent: an int
        :return: a boolean
        """
        return False

    def lockout_msg(self):
        """
        Display the lockout message.
        """
        print("Notification: You have exceeded your budget limit.")

    def is_lockout_action_required(self):
        """
        Returns always False since Angel never gets locked out of their budget
        :return: a boolean
        """
        return False

    def is_exceed_warning_threshold(self, limit, spent):
        """
        Returns true if the budget exceed more than warning threshold.
        :param limit: a float
        :param spent: a float
        """
        return True if self._warning_threshold * limit + spent <= 0 else False

    def warning_msg(self):
        print(f'Warning: You have exceeded {int(self._warning_threshold * 100)}% of this budget.')


class Rebel(User):
    """
    A Rebel class.
    """
    def __init__(self, name: str, dob: datetime, bank_account_number: str, warning_threshold: float):
        super().__init__(name, dob, bank_account_number, warning_threshold)

    def is_over_account_lockout_threshold(self, number_of_locked_budget, num_budget_types):
        """
        Returns True if the user exceed their budget in 2 or more categories, otherwise False.
        :param number_of_locked_budget: an int
        :param num_budget_types: an int
        :return: a boolean
        """
        return number_of_locked_budget >= num_budget_types or number_of_locked_budget >= 2

    def is_over_lockout_threshold(self, limit, spent):
        """
        Return True if the user exceed a budget category, otherwise False.
        :param limit: an int
        :param spent: an int
        :return: a boolean
        """
        return limit + spent <= 0

    def lockout_msg(self):
        """
        Display the lockout message.
        """
        print("Locked: You have exceeded your budget limit.")

    def is_lockout_action_required(self):
        """
        Returns always True since Rebel can get locked out of their budget.
        :return: a boolean
        """
        return True

    def is_exceed_warning_threshold(self, limit, spent):
        """
        Returns true if the budget exceed more than warning threshold.
        :param limit: a float
        :param spent: a float
        """
        return True if self._warning_threshold * limit + spent <= 0 else False

    def warning_msg(self):
        print(f'Warning: You have exceeded {int(self._warning_threshold * 100)}% of this budget.')


class TroubleMaker(User):
    """
    A TroubleMaker class.
    """
    def __init__(self, name: str, dob: datetime, bank_account_number: str, warning_threshold: float):
        super().__init__(name, dob, bank_account_number, warning_threshold)

    def is_over_account_lockout_threshold(self, number_of_locked_budget, num_budget_types):
        """
        Returns always false.
        :param number_of_locked_budget: an int
        :param num_budget_types: an int
        :return: a boolean
        """
        return False

    def is_over_lockout_threshold(self, limit, spent):
        """
        Return True if the user exceed 120% of the budget category, otherwise False.
        :param limit: an int
        :param spent: an int
        :return: a boolean
        """
        return limit * 1.2 + spent <= 0

    def lockout_msg(self):
        """
        Display the lockout message.
        """
        print("Locked: You have been locked out of this budget category.")

    def is_lockout_action_required(self):
        """
        Returns always True since TroubleMaker can get locked out of their budget.
        :return: a boolean
        """
        return True

    def is_exceed_warning_threshold(self, limit, spent):
        """
        Returns true if the budget exceed more than warning threshold.
        :param limit: a float
        :param spent: a float
        """
        return True if self._warning_threshold * limit + spent <= 0 else False

    def warning_msg(self):
        print(f'Warning: You have exceeded {int(self._warning_threshold * 100)}% of this budget.')
