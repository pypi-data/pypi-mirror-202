class LabelfError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class LabelfAPIError(LabelfError):
    def __init__(self, message: str):
        super().__init__(message)
