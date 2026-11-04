class CategoryAlreadyExistsException(Exception):
    def __init__(self, message: str = "Category with the same name already exists."):
        self.message = message
        super().__init__(self.message)


class CategoryCreationFailedException(Exception):
    def __init__(self, message: str = "Failed to create category."):
        self.message = message
        super().__init__(self.message)


class GetAllCategoriesByTeamIdNotFoundException(Exception):
    def __init__(self, message: str = "No categories found for the given team ID."):
        self.message = message
        super().__init__(self.message)


class CategoryRetrievalException(Exception):
    def __init__(self, message: str = "Failed to retrieve categories."):
        self.message = message
        super().__init__(self.message)


class CategoryNotFoundException(Exception):
    def __init__(self, message: str = "Category not found."):
        self.message = message
        super().__init__(self.message)


class CategoryUpdateException(Exception):
    def __init__(self, message: str = "Failed to update category."):
        self.message = message
        super().__init__(self.message)


class CategoryDeletionException(Exception):
    def __init__(self, message: str = "Failed to delete category."):
        self.message = message
        super().__init__(self.message)
