"""
    Module containing custom exceptions for handling email-related errors.
"""


class InvalidEmailSubject(Exception):
    """
        Exception raised when an email subject is invalid.

        This may be due to the subject being too long or containing invalid characters.
    """
    pass


class InvalidEmailReceiverAddress(Exception):
    """
        Exception raised when an email receiver address is invalid.

        This may be due to the address being improperly formatted or not existing.
    """
    pass


class InvalidEmailBody(Exception):
    """
        Exception raised when an email body is invalid.

        This may be due to the body being too long or containing invalid characters.
    """
    pass
