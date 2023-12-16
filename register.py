from user_type import UserType
from bank_account_type import BankAccountType
from budget_types import BudgetType
from budget import *
from user import *
from bank_account import *
import datetime


class Register:
    """
    This class is responsible for guiding a user through the registration process.
    """
    @staticmethod
    def register_user(bank_account_catalogue, budget_catalogue):
        """
        Takes various inputs from user to create a User
        :return: User
        """
        print("Welcome to FAM! Please register an account.")

        # Get bank account info
        user_bank_account = Register.set_user_bank_account(bank_account_catalogue)

        # Set User info
        user = Register.set_user_type(user_bank_account)

        # Set users' budgets
        Register.set_user_budgets(budget_catalogue, user_bank_account)

        return user

    @staticmethod
    def set_user_type(bank_account_number: str) -> User:
        """
        Returns a User object according to the given information.
        :param bank_account_number: a string
        :return: a User
        """
        # Get name
        name = input("Enter your name: ")

        # Get dob
        year = int(input("Enter your birth year in YYYY format: "))
        month = int(input("Enter your birth month in MM format: "))
        day = int(input("Enter your birth-day in DD format: "))
        dob = datetime.datetime(year, month, day)

        # Get user type
        user_type_accepted = False
        user_type = 0
        while not user_type_accepted:
            for user_type in list(UserType):
                print(user_type.value, "\b.", user_type.name)
            user_type = int(input("Select a user type: "))
            if user_type == UserType.ANGEL.value and not Register.eligible_for_angel(dob):
                print("ERROR: You are too young to be an Angel. Please select other user types.")
            else:
                user_type_accepted = True

        # Return User according to the given user type
        user_type_map = {
            1: Rebel(name, dob, bank_account_number, 0.5),
            2: Angel(name, dob, bank_account_number, 0.9),
            3: TroubleMaker(name, dob, bank_account_number, 0.75)
        }
        user_register_operation = user_type_map[user_type]
        return user_register_operation

    @staticmethod
    def set_user_bank_account(bank_account_catalogue):
        for bank_account_type in list(BankAccountType):
            print(bank_account_type.value, "\b.", bank_account_type.name)

        bank_account_type = int(input("Select a bank account type: "))
        bank_attributes = {
            "bank_acc_num": input("Enter bank account number: "),
            "bank_name": input("Enter bank name: "),
            "bank_bal": float(input("Enter bank balance: $"))
        }
        # Create a bank account under in the bank_account_catalogue
        bank_account_type_map = {
            1: Chequing(**bank_attributes),
            2: Saving(**bank_attributes)
        }
        bank_account_operation = bank_account_type_map[bank_account_type]
        bank_account_catalogue.add_bank_account(bank_account_operation)
        return bank_attributes["bank_acc_num"]

    @staticmethod
    def set_user_budgets(budget_catalogue, user_bank_account):
        for budget_type in list(BudgetType):
            print(budget_type.value, "\b.", budget_type.name)
            limit = float(input("Enter limit for budget: $"))

            if budget_type.name == BudgetType.GAMES_ENTERTAINMENT.name:
                games_entertainment = GamesEntertainment(limit, user_bank_account)
                budget_catalogue.add_budget(games_entertainment)
            if budget_type.name == BudgetType.CLOTHING_ACCESSORIES.name:
                clothing_accessories = ClothingAccessories(limit, user_bank_account)
                budget_catalogue.add_budget(clothing_accessories)
            if budget_type.name == BudgetType.EATING_OUT.name:
                eating_out = EatingOut(limit, user_bank_account)
                budget_catalogue.add_budget(eating_out)
            if budget_type.name == BudgetType.MISCELLANEOUS.name:
                miscellaneous = Miscellaneous(limit, user_bank_account)
                budget_catalogue.add_budget(miscellaneous)

    @staticmethod
    def eligible_for_angel(dob: datetime) -> bool:
        """
        Return if the user is eligible to be an Angel.
        :param dob: a datetime
        :return: true if eligible to be an Angel, false otherwise
        """
        return Register.get_age(dob) >= 16
    #

    @staticmethod
    def get_age(birthdate) -> int:
        """
        Returns the user's age calculated from dob.
        :param birthdate: a datetime
        :return: an int
        """
        today = datetime.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
