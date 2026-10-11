class SubAccountHistoryRetrievalException(Exception):
    '''Exception raised when there is an error retrieving sub-account history.'''
    def __init__(self, message: str):
        super().__init__(message)

class RotateSubAccountDeksException(Exception):
    '''Exception raised when there is an error rotating sub-account data keys.'''
    def __init__(self, message: str):
        super().__init__(message)
