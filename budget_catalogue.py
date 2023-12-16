from budget import *


class BudgetCatalogue:
    """
    This class houses a list of all budgets.
    """
    budget_type_map = {
        1: GamesEntertainment,
        2: ClothingAccessories,
        3: EatingOut,
        4: Miscellaneous
    }

    _budget_list = []

    @classmethod
    def get_budgets(cls):
        """
        Getter for budget list.
        :return: budget list
        """
        return cls._budget_list

    @classmethod
    def get_budgets_by_account_num(cls, bank_account_number: str) -> list[Budget]:
        """
        Retrieves all budgets for a bank account number and displays them.
        :param bank_account_number: a string
        """
        budget_list = []
        for budget in cls.get_budgets():
            if budget.bank_account_number == bank_account_number:
                budget_list.append(budget)
        return budget_list

    @classmethod
    def filter_budget_by_bank_account_and_category(cls, bank_account_number: str, map_key) -> Budget:
        """
        Filter the budget by the given category and returns it.
        :param bank_account_number: a string
        :param map_key: an int
        """
        for budget in cls.get_budgets():
            if budget.bank_account_number == bank_account_number \
                    and type(budget) == BudgetCatalogue.budget_type_map[map_key]:
                return budget

    @classmethod
    def adjust_budget_details(cls, bank_account_number: str, budget_type: int, amount: float) -> None:
        """
        Updates the spent amount of the given budget.
        :param bank_account_number: a string
        :param budget_type: a int
        :param amount: float
        """
        user_budget_list = cls.get_budgets_by_account_num(bank_account_number)

        for budget in user_budget_list:
            if type(budget) == BudgetCatalogue.budget_type_map[budget_type]:
                budget.add_spent(amount)

    @classmethod
    def add_budget(cls, budget):
        """
        Adds a budget to the budget list.
        :param budget: a Budget object
        """
        cls._budget_list.append(budget)
