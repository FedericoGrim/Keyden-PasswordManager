class CreateCategoryException(Exception):
    def __init__(self, message: str = "Failed to create category.") -> None:
        self.message = message
        super().__init__(self.message)


class CategoryRetrievalException(Exception):
    def __init__(self, message: str = "Failed to retrieve categories.") -> None:
        self.message = message
        super().__init__(self.message)


class CategoryUpdateException(Exception):
    def __init__(self, message: str = "Failed to update category.") -> None:
        self.message = message
        super().__init__(self.message)


class CategoryDeletionException(Exception):
    def __init__(self, message: str = "Failed to delete category.") -> None:
        self.message = message
        super().__init__(self.message)
