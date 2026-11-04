class CreateSubAccountCategoryException(Exception):
    def __init__(self, message: str = "Failed to create subacc category.") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryRetrievalException(Exception):
    def __init__(self, message: str = "Failed to retrieve subacc categories.") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryUpdateException(Exception):
    def __init__(self, message: str = "Failed to update subacc category.") -> None:
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryDeletionException(Exception):
    def __init__(self, message: str = "Failed to delete subacc category.") -> None:
        self.message = message
        super().__init__(self.message)
