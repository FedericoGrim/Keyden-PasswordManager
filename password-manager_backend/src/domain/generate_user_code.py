import secrets
import string

USER_CODE_LENGTH = 10
_ALPHABET = string.ascii_letters + string.digits


def generate_user_code(length: int = USER_CODE_LENGTH) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))
