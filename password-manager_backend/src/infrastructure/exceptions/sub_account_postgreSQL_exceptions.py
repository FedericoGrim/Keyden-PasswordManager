class SubAccountAlreadyExistsException(Exception):
    def __init__(self, message: str = "SubAccount already exists") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountCreationFailedException(Exception):
    def __init__(self, message: str = "SubAccount creation failed") -> None:
        self.message = message
        super().__init__(self.message)


class GetAllSubAccountsByTeamIdNotFoundException(Exception):
    def __init__(
        self, message: str = "No subaccounts found for the given user ID"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountNotFoundException(Exception):
    def __init__(self, message: str = "SubAccount not found") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountUpdateException(Exception):
    def __init__(self, message: str = "Error updating subaccount") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountDeletionException(Exception):
    def __init__(self, message: str = "Error deleting subaccount") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountRetrievalException(Exception):
    def __init__(self, message: str = "Error retrieving subaccounts") -> None:
        self.message = message
        super().__init__(self.message)
