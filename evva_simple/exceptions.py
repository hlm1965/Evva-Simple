"""
Custom exceptions for Evva-Simple
"""


class EvvaAPIError(Exception):
    """Base exception for all Evva API errors"""
    pass


class EvvaAuthenticationError(EvvaAPIError):
    """Raised when authentication fails"""
    pass


class EvvaNotFoundError(EvvaAPIError):
    """Raised when a resource is not found"""
    pass


class EvvaValidationError(EvvaAPIError):
    """Raised when request validation fails"""
    pass
