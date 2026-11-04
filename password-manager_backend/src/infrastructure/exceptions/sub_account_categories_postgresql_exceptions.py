class SubAccountCategoryAlreadyExistsException(Exception):
    def __init__(
        self,
        message: str = "SubAccountCategory with the same subaccount and category already exists.",
    ):
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryCreationFailedException(Exception):
    def __init__(self, message: str = "Failed to create subacc category."):
        self.message = message
        super().__init__(self.message)


class GetAllCategoriesBySubAccountIdNotFoundException(Exception):
    def __init__(
        self, message: str = "No categories found for the given subaccount ID."
    ):
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryRetrievalException(Exception):
    def __init__(self, message: str = "Failed to retrieve subacc categories."):
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryNotFoundException(Exception):
    def __init__(self, message: str = "SubAccountCategory not found."):
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryUpdateFailedException(Exception):
    def __init__(self, message: str = "Failed to update subacc category."):
        self.message = message
        super().__init__(self.message)


class SubAccountCategoryDeletionFailedException(Exception):
    def __init__(self, message: str = "Failed to delete subacc category."):
        self.message = message
        super().__init__(self.message)
