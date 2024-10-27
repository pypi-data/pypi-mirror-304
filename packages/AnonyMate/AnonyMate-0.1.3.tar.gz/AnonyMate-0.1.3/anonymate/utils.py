# anonymate/utils.py

def mask_partial(text: str, visible_start: int = 1, visible_end: int = 1, mask_char: str = "*") -> str:
    """
    Partially masks a text, showing only the specified number of starting and ending characters.
    
    Args:
        text (str): The original text to be masked.
        visible_start (int): Number of characters to keep visible at the start.
        visible_end (int): Number of characters to keep visible at the end.
        mask_char (str): The character to use for masking.

    Returns:
        str: Partially masked text.
    
    Example:
        mask_partial("SensitiveData", 2, 2) -> "Se********ta"
    """
    if len(text) <= visible_start + visible_end:
        return text  # No masking needed if text is too short
    return text[:visible_start] + mask_char * (len(text) - visible_start - visible_end) + text[-visible_end:]

def validate_email(email: str) -> bool:
    """
    Simple email validation to check if an email has the correct format.
    
    Args:
        email (str): The email to validate.
    
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_regex, email))

def mask_email(email: str) -> str:
    """
    Mask an email address, leaving the first character of the username and domain visible.
    
    Args:
        email (str): The email address to mask.
    
    Returns:
        str: Masked email with only the first character of the username and domain visible.
    
    Example:
        mask_email("example@example.com") -> "e******@e******.com"
    """
    if "@" not in email:
        return email  # Return as is if it's not a valid email format
    username, domain = email.split("@")
    return f"{username[0]}{'*' * (len(username) - 1)}@{domain[0]}{'*' * (len(domain.split('.')[0]) - 1)}.{domain.split('.')[-1]}"

def generate_salt(length: int = 16) -> str:
    """
    Generate a random salt string for hashing purposes.
    
    Args:
        length (int): The length of the salt string. Default is 16.
    
    Returns:
        str: Randomly generated salt string.
    """
    import os
    return os.urandom(length).hex()
