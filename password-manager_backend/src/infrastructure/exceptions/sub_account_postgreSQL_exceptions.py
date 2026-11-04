class SubAccountAlreadyExistsException(Exception):
    def __init__(self, message: str = "SubAccount already exists"):
        self.message = message
        super().__init__(self.message)


class SubAccountCreationFailedException(Exception):
    def __init__(self, message: str = "SubAccount creation failed"):
        self.message = message
        super().__init__(self.message)


class GetAllSubAccountsByTeamIdNotFoundException(Exception):
    def __init__(self, message: str = "No subaccounts found for the given user ID"):
        self.message = message
        super().__init__(self.message)


class SubAccountNotFoundException(Exception):
    def __init__(self, message: str = "SubAccount not found"):
        self.message = message
        super().__init__(self.message)


class SubAccountUpdateException(Exception):
    def __init__(self, message: str = "Error updating subaccount"):
        self.message = message
        super().__init__(self.message)


class SubAccountDeletionException(Exception):
    def __init__(self, message: str = "Error deleting subaccount"):
        self.message = message
        super().__init__(self.message)


class SubAccountRetrievalException(Exception):
    def __init__(self, message: str = "Error retrieving subaccounts"):
        self.message = message
        super().__init__(self.message)
