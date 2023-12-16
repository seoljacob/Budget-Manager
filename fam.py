from budget_catalogue import BudgetCatalogue
from bank_account_catalogue import BankAccountCatalogue
from transaction_catalogue import TransactionCatalogue
from register import Register
from user import User
from budget_types import BudgetType


class Fam:
    """
    The Fam class. It allows users to register a new user, keep track of all the spending/transactions
    on their bank account, and lock the account if certain conditions are met.
    """
    MAIN_MENU = ['Register a user', 'Select a user', 'Exit Program']
    ACCOUNT_MENU = ['View Budget', 'Record a Transaction', 'View Transactions by Budget',
                    'View Bank Account Details', 'Go back to previous menu']

    def __init__(self, bank_account_catalogue: BankAccountCatalogue, budget_catalogue: BudgetCatalogue,
                 transaction_catalogue: TransactionCatalogue):
        """
        Initialize the Fam class with bank_account_catalogue and budget_catalogue.
        :param bank_account_catalogue: a BankAccountCatalogue object
        :param budget_catalogue: a BudgetCatalogue object
        """
        self._user_list = []
        self._bank_account_Catalogue = bank_account_catalogue
        self._budget_catalogue = budget_catalogue
        self._transaction_catalogue = transaction_catalogue

    @property
    def user_list(self) -> list:
        """
        Return a list of users.
        :return: a list of User objects
        """
        return self._user_list

    @property
    def bank_account_catalogue(self) -> BankAccountCatalogue:
        """
        Return a BankAccountCatalogue object.
        :return: a BankAccountCatalogue object
        """
        return self._bank_account_Catalogue

    @property
    def budget_catalogue(self) -> BudgetCatalogue:
        """
        Return a BudgetCatalogue object.
        :return: a BudgetCatalogue object
        """
        return self._budget_catalogue

    @property
    def transaction_catalogue(self) -> TransactionCatalogue:
        """
        Return a TransactionCatalogue object.
        :return: a TransactionCatalogue object
        """
        return self._transaction_catalogue

    def display_main_menu(self) -> None:
        """
        Display the user menu allowing the user to register a new user and select the user from the user list.
        """
        user_input = None
        while user_input != len(Fam.MAIN_MENU):
            print(f"\nWelcome to Family Appointed Moderator!")
            print("-----------------------")
            for count, menu in enumerate(Fam.MAIN_MENU):
                print(f"{count + 1}. {menu}")

            try:
                user_input = int(input(f"Please enter a number (1 - {len(Fam.MAIN_MENU)}): "))
                if user_input == Fam.MAIN_MENU.index('Register a user') + 1:
                    self._add_user(Register.register_user(self.bank_account_catalogue, self.budget_catalogue))
                elif user_input == Fam.MAIN_MENU.index('Select a user') + 1:
                    if len(self.user_list) == 0:
                        print('\nError: There is no available user account')
                    elif user := self._select_user():
                        self._display_account_menu(user)
                elif user_input == Fam.MAIN_MENU.index('Exit Program') + 1:
                    print(f"Thank you.")
                else:
                    print(f"Error: Could not process the input. Please enter a number from (1 - {len(Fam.MAIN_MENU)}).")
            except ValueError or TypeError:
                print(f'Error: Could not process the input.')

    def _add_user(self, user: User) -> None:
        """
        Add user to the user list.
        :param user: a User object
        """
        self.user_list.append(user)

    def _select_user(self) -> User or None:
        """
        Get user selection from the user list.
        :return: a User object
        """
        user_input = None
        while user_input != len(self.user_list) + 1:

            print(f"\nSelect a user")
            print("-----------------------")
            for count, user in enumerate(self.user_list):
                print(f"{count + 1}. {user.name}")

            print(f"{len(self.user_list) + 1}. Go back to previous menu")

            try:
                user_input = int(input(f"Please enter a number: "))
                if user_input - 1 != len(self.user_list):
                    return self.user_list[user_input - 1]
                elif user_input - 1 == len(self.user_list):
                    return None
            except ValueError or TypeError:
                print(f'Error: Could not process the input.')

    def _display_account_menu(self, user: User) -> None:
        """
        Display the user account menu allowing the user to either view budgets, record a transaction,
        view transactions by budget, or view bank account details.
        :param user: a User object
        """
        user_input = None
        while user_input != len(Fam.ACCOUNT_MENU):

            print(f"\n{user.name}'s Account")
            print("-----------------------")
            for count, menu in enumerate(Fam.ACCOUNT_MENU):
                print(f"{count + 1}. {menu}")

            try:
                user_input = int(input(f"Please enter a number (1 - {len(Fam.ACCOUNT_MENU)}) "))

                if user_input - 1 == Fam.ACCOUNT_MENU.index('View Budget'):
                    self._view_budget_option(user)

                elif user_input - 1 == Fam.ACCOUNT_MENU.index('Record a Transaction'):
                    self._record_transaction_option(user)

                elif user_input - 1 == Fam.ACCOUNT_MENU.index('View Transactions by Budget'):
                    self._view_transactions_by_budget(user)

                elif user_input - 1 == Fam.ACCOUNT_MENU.index('View Bank Account Details'):
                    self._view_bank_account_detail_option(user)

            except Exception as e:
                print(f'Error: Could not process the input.\n {e}')

    def _view_budget_option(self, user: User) -> None:
        """
        Shows the user the current status of their budgets (locked or not) in addition to the amount spent,
        amount left, and the total amount allocated to the budget.
        """
        user_budget_list = self.budget_catalogue.get_budgets_by_account_num(user.bank_account_number)
        for budget in user_budget_list:
            print(budget)

    def _record_transaction_option(self, user: User) -> None:
        """
        Allows the user to enter new transaction details.
        :param user: a User
        """
        # Check if the user's bank account is locked
        if self.bank_account_catalogue.is_users_account_locked(user.bank_account_number):
            print("Warning: Could not add another transaction since your account is locked.")
            return
        else:
            # Add transaction and append it to the transaction list under the transaction_catalogue
            self.transaction_catalogue.add_transaction(user)

    def _view_transactions_by_budget(self, user: User) -> None:
        """
        Allows the user to select the budget category and view all the transactions to date in that category.
        :param user: a User
        """
        # Get user transactions
        user_transactions = self.transaction_catalogue.get_user_transactions(user.bank_account_number)
        return_list = []

        # Let user select the budget category
        for budget_type in list(BudgetType):
            print(budget_type.value, "\b.", budget_type.name)
        selected = int(input("Select the budget category you'd like to explore: "))
        for transaction in user_transactions:
            if transaction.budget_category == selected:
                return_list.append(transaction)
        print(f"======== Transactions Under {BudgetType(selected).name} ========")
        for transaction in return_list:
            print(transaction)

    def _view_bank_account_detail_option(self, user: User) -> None:
        """
        Prints out the bank account details of the user and all transactions conducted to
        date alongside the closing balance.
        :param user: a User
        """
        print("======== Bank account Details ========\n")
        print(self._bank_account_Catalogue.get_user_bank_account(user.bank_account_number))
        print("\n======== Budget Status ========")
        self._view_budget_option(user)
        print("======== All Transactions ========")
        self.transaction_catalogue.print_user_transactions(user.bank_account_number)
