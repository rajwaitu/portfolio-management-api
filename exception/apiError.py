
class APIError(Exception):
    """Exception raised for errors processing the request.

    Attributes:
        statusCode -- HTTP Status Code
        message -- explanation of the error
    """

    def __init__(self, statusCode, message="Exception occeued while processing the request"):
        self.statusCode = statusCode
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.statusCode} -> {self.message}'