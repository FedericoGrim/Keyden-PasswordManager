class CreateSubAccountException(Exception):
    """Exception raised when there is an error creating a subaccount."""

    def __init__(self, message: str):
        super().__init__(message)


class SubAccountRetrievalException(Exception):
    """Exception raised when there is an error retrieving a subaccount."""

    def __init__(self, message: str):
        super().__init__(message)


class SubAccountUpdateException(Exception):
    """Exception raised when there is an error updating a subaccount."""

    def __init__(self, message: str):
        super().__init__(message)


class SubAccountDeletionException(Exception):
    """Exception raised when there is an error deleting a subaccount."""

    def __init__(self, message: str):
        super().__init__(message)
