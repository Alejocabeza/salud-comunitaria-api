import secrets
import string

def generate_secure_password(length: int = 8) -> str:
    """
    Generate a secure random password
    
    Args:
        length (int): Length of the password to generate
        
    Returns:
        str: A secure random password containing letters and digits
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length)) 