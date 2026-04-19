class IEEEPapersError(Exception):
    """Base exception."""


class IEEEApiError(IEEEPapersError):
    """IEEE API request failed."""


class PaperValidationError(IEEEPapersError):
    """Paper data failed Pydantic validation."""
