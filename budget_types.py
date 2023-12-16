from enum import Enum


class BudgetType(Enum):
    """
    Budget categories for each bank account.
    """
    GAMES_ENTERTAINMENT = 1
    CLOTHING_ACCESSORIES = 2
    EATING_OUT = 3
    MISCELLANEOUS = 4
