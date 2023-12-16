from transaction import Transaction
from budget_types import BudgetType
from budget_catalogue import BudgetCatalogue
from bank_account_catalogue import BankAccountCatalogue
import time


class TransactionCatalogue:
    """
    This class houses a list of all transactions.
    """

    _transactions = []

    def get_transactions(self):
        """
        Getter for transaction list.
        :return: transaction list
        """
        return self._transactions

    def add_transaction(self, user):
        """
        Adds a transaction to the transaction list.
        """
        user_bank_account = BankAccountCatalogue.get_user_bank_account(user.bank_account_number)

        while True:
            # Get current timestamp
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Get budget type
            for budget_type in list(BudgetType):
                print(budget_type.value, "\b.", budget_type.name)
            budget_category = int(input("Select a budget category: "))

            target_budget = \
                BudgetCatalogue.filter_budget_by_bank_account_and_category(user.bank_account_number, budget_category)

            # Exits to the main menu if the budget is locked out.
            if user.is_over_lockout_threshold(target_budget.limit, target_budget.spent):
                user.lockout_msg()
                if user.is_lockout_action_required():
                    return
            elif target_budget.is_budget_exceeded():
                print(f"Notification: You have exceeded your budget limit of ${target_budget.limit:.2f}")

            # Get transaction amount
            amount = float(input("Enter amount: $"))
            if amount <= 0:
                print("Please enter a positive, non-zero number.")
                break

            # Stop transaction from being recorded if the user doesn't have sufficient funds
            if amount > user_bank_account.bank_bal:
                print("Notification: You have insufficient funds.")
                print(f"Current bank account balance: ${user_bank_account.bank_bal}")
                break

            # Adjust a Budget object
            BudgetCatalogue.adjust_budget_details(user.bank_account_number, budget_category, amount)

            # Get merchant
            merchant = input("Enter merchant: ")

            # Create a Transaction
            transaction = Transaction(current_time, amount, budget_category, merchant, user.bank_account_number)

            # Add the Transaction to the transaction list
            self._transactions.append(transaction)

            # check if the budget is locked out after this transaction
            target_budget = \
                BudgetCatalogue.filter_budget_by_bank_account_and_category(user.bank_account_number, budget_category)

            has_warning_or_lockout = False

            # Adjust a bank account balance
            user_bank_account.bank_bal -= amount

            if user.is_over_lockout_threshold(target_budget.limit, target_budget.spent):
                user.lockout_msg()
                has_warning_or_lockout = True
            elif target_budget.is_budget_exceeded():
                print(f"Notification: You have exceeded your budget limit of ${target_budget.limit:.2f}")
                has_warning_or_lockout = True
            elif user.is_exceed_warning_threshold(target_budget.limit, target_budget.spent):
                user.warning_msg()
                has_warning_or_lockout = True

            # Prints the transactions if the budget has any warning or notification
            if has_warning_or_lockout:
                self._print_filtered_transactions_by_budget(user.bank_account_number, budget_category)

            # Lock the user's account if the user type's lockout rule is met
            self._is_account_lockout_threshold_over(user, user_bank_account)

            # Lock the user's account if the bank account type's lockout rule is met
            user_bank_account.is_balance_negative()
            return user_bank_account.is_over_limit(self)

    def get_user_transactions(self, bank_account_number) -> list[Transaction]:
        """
        Retrieves all transactions for a bank account number and displays them.
        :param bank_account_number: a string
        :return: a list of users' transactions
        """
        user_transactions = []
        for transaction in self.get_transactions():
            if transaction.bank_num == bank_account_number:
                user_transactions.append(transaction)
        return user_transactions

    def print_user_transactions(self, bank_account_number) -> None:
        """
        Print out all transactions belong to the user.
        :param bank_account_number: a string
        """
        trans_list = self.get_user_transactions(bank_account_number)
        for transaction in trans_list:
            print(f"======== Transaction {trans_list.index(transaction) + 1} ========")
            print(transaction)

    def _print_filtered_transactions_by_budget(self, bank_account_number, budget_category):
        """
        Prints the transactions for the given budget
        :param bank_account_number: a string
        :param budget_category: an int
        """
        user_transactions = self.get_user_transactions(bank_account_number)
        filtered_transactions = \
            [transaction for transaction in user_transactions if transaction.budget_category == budget_category]
        print(f"======== Transactions under {BudgetType(budget_category).name} ========")
        for transaction in filtered_transactions:
            print(transaction)

    @staticmethod
    def _is_account_lockout_threshold_over(user, user_bank_account):
        """
        Locks the user's account if the user type's account lock out rule is met.

        :param user: a User
        :param user_bank_account: a BankAccount
        """
        budgets = BudgetCatalogue.get_budgets_by_account_num(user.bank_account_number)
        num_budgets = len(budgets)
        locked_budget = [user.is_over_lockout_threshold(budget.limit, budget.spent) for budget in budgets]
        if user.is_over_account_lockout_threshold(sum(locked_budget), num_budgets):
            print('Notification: Your account is locked.')
            user_bank_account.lock_account()
