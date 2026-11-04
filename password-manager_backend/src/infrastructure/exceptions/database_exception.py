class PostgreSqlConnectionException(Exception):
    """
    Exception raised for errors in the PostgreSQL connection.
    This exception is typically raised when there is an issue connecting to the PostgreSQL database.
    It can be used to handle connection errors specifically in the context of PostgreSQL operations.
    This can include errors related to network issues, authentication failures, or database server unavailability.

    Args:
        message (str): Explanation of the error. Defaults to "PostgreSQL connection error occurred".
    """  # noqa: E501

    def __init__(self, message: str = "PostgreSQL connection error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class PostgreSqlException(Exception):
    """
    Exception raised for general PostgreSQL errors.
    This exception is typically raised when there is an error during PostgreSQL operations.
    It can be used to handle errors that are not specific to connection issues.
    This can include errors related to queries, transactions, or other database operations.

    Args:
        message (str): Explanation of the error. Defaults to "PostgreSQL error occurred".
    """  # noqa: E501

    def __init__(self, message: str = "PostgreSQL error occurred") -> None:
        self.message = message
        super().__init__(self.message)
