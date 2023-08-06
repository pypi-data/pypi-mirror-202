import re


def is_valid_email(email):
    """
        Checks if the given email is a valid email address.

        Args:
            email (str): The email address to check.

        Returns:
            bool: True if the email is valid, False otherwise.
    """
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(email_regex.match(email))
