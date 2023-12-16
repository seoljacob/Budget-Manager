from bank_account import BankAccount


class BankAccountCatalogue:
    """
    This class houses a list of all bank accounts.
    """
    bank_accounts = []

    @classmethod
    def get_bank_accounts(cls):
        """
        Getter for bank accounts
        :return: a list of bank accounts
        """
        return cls.bank_accounts

    @classmethod
    def get_user_bank_account(cls, bank_account_number: str) -> BankAccount:
        """
        Retrieves all bank accounts for a bank account number and displays them.
        :param bank_account_number: a string
        :return: a BankAccount
        """
        for bank_account in cls.get_bank_accounts():
            if bank_account.bank_account_number == bank_account_number:
                return bank_account

    @classmethod
    def is_users_account_locked(cls, bank_account_number: str) -> bool:
        """
        Returns if the users bank account is locked.
        :param bank_account_number: a string
        :return: a boolean
        """
        user_bank_account = cls.get_user_bank_account(bank_account_number)
        return user_bank_account.is_locked

    @classmethod
    def add_bank_account(cls, bank_account: BankAccount):
        """
        Adds a new bank account to the list of bank accounts.
        :param bank_account: a BankAccount object.
        """
        BankAccountCatalogue.bank_accounts.append(bank_account)

    @classmethod
    def remove_bank_account(cls, bank_acc_num):
        """
        Removes a bank account given a bank account number.
        :param bank_acc_num: a string
        """
        for index, bank_account in enumerate(BankAccountCatalogue.bank_accounts):
            if bank_account.bank_acc_num == bank_acc_num:
                del BankAccountCatalogue.bank_accounts[index]
                break
