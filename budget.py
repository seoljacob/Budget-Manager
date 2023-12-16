class Budget:
    def __init__(self, limit: float, bank_account_number: str):
        self._spent = 0
        self._limit = limit
        self._bank_account_number = bank_account_number

    @property
    def spent(self) -> float:
        """
        Returns the amount of spent from each Budget.
        :return: a float
        """
        return self._spent

    @property
    def bank_account_number(self):
        return self._bank_account_number

    @property
    def limit(self) -> float:
        """
        Returns the limit of the Budget.
        :return: a float
        """
        return self._limit

    def add_spent(self, amount):
        self._spent -= amount

    def is_budget_exceeded(self):
        return self.limit + self.spent <= 0

    def __str__(self):
        return (f"---- {self.__class__.__name__} ----\n"
                f"Limit: ${self.limit:.2f}\n"
                f"The amount spent: ${-self.spent:.2f}"
                f"  For Bank Account: {self.bank_account_number}\n")


class GamesEntertainment(Budget):
    pass


class ClothingAccessories(Budget):
    pass


class EatingOut(Budget):
    pass


class Miscellaneous(Budget):
    pass
