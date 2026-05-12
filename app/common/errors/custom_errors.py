class DatabaseOperationError(Exception):
    """when database fails to execute a query"""
    def __init__(self, *,  message: str):
        self.message = message
        super().__init__(self.message)
        
class ResourceNotFoundException(Exception):
    """Raised when a requested reource does not exist"""
    def __init__(self, *,  message : str):
        self.message = message
        super().__init__(self.message)
        
class DuplicateEmailException(Exception):
    """Raised when data conflicts"""
    def __init__(self, *,  message : str):
        self.message = message
        super().__init__(self.message)
        