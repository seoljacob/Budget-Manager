from fam import Fam
from budget_catalogue import BudgetCatalogue
from bank_account_catalogue import BankAccountCatalogue
from transaction_catalogue import TransactionCatalogue


class Driver:
    """
    Driver class drives
    """
    fam = Fam(BankAccountCatalogue(), BudgetCatalogue(), TransactionCatalogue())
    fam.display_main_menu()


def main():
    """
    Driver of the FAM.
    """
    Driver()


if __name__ == "__main__":
    main()
