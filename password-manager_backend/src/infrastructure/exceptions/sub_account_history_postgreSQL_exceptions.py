class SubAccountHistoryCreationFailedException(Exception):
    def __init__(
        self, message: str = "SubAccount history entry creation failed"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountHistoryRetrievalException(Exception):
    def __init__(self, message: str = "Error retrieving sub-account history") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountHistoryNotFoundException(Exception):
    def __init__(self, message: str = "SubAccount history entry not found") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountHistoryDekUpdateException(Exception):
    def __init__(
        self, message: str = "Error updating sub-account history data key"
    ) -> None:
        self.message = message
        super().__init__(self.message)
