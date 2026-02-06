class BaseApiException(Exception):
    """
    Base exception for all Api exceptions
    """

    def __init__(
        self,
        error_code: str,
        message: str,
        payload: dict | None = None,
        type: str | None = None,
    ):
        self.error_code = error_code
        self.message = message
        self.payload = payload or {}
        self.type = type or "callback_answer"
        super().__init__(message)

    def __str__(self) -> str:
        message = self.message
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"
